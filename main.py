import logging
from pathlib import Path
import multiprocessing as mp
from typing import List, Optional
from tqdm import tqdm
from pubmed_tools.parser.xml_parser import PubmedParser
from pubmed_tools.scan.xml_scanner import scan_xml_files
from pubmed_tools.export.json_exporter import JsonExporter
from pubmed_tools.export.tsv_exporter import TsvExporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_single_file(xml_file: str) -> List[dict]:
    """处理单个XML文件"""
    try:
        parser = PubmedParser()
        articles = parser.parse_file(xml_file, show_progress=False)
        return articles
    except Exception as e:
        logger.error("处理文件 %s 时发生错误: %s", xml_file, e)
        return []

def process_pubmed_files(input_dir: str, output_dir: str, num_workers: Optional[int] = None):
    """
    并行处理PubMed XML文件并导出结果
    
    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
        num_workers: 并行处理的线程数，默认为CPU核心数
    """
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 扫描XML文件
        logger.info("开始扫描XML文件...")
        xml_files = scan_xml_files(input_dir)
        total_files = len(xml_files)
        logger.info("找到 %d 个XML文件", total_files)
        
        # 设置并行进程数
        if num_workers is None:
            num_workers = mp.cpu_count()
        num_workers = min(num_workers, total_files)  # 不超过文件数
        logger.info("使用 %d 个进程并行处理", num_workers)
        
        all_articles = []
        
        # 创建进程池并处理文件
        with mp.Pool(num_workers) as pool:
            # 使用imap_unordered获取结果迭代器
            results_iter = pool.imap_unordered(process_single_file, xml_files)
            
            # 使用tqdm显示总体进度
            with tqdm(total=total_files, desc="处理XML文件") as pbar:
                for articles in results_iter:
                    all_articles.extend(articles)
                    pbar.update(1)
                    pbar.set_postfix({"已处理文献": len(all_articles)})
        
        # 导出结果
        if all_articles:
            logger.info("开始导出 %d 篇文献...", len(all_articles))
            
            # JSON导出
            json_path = output_path / "pubmed_articles.json"
            json_exporter = JsonExporter()
            json_exporter.export(all_articles, str(json_path))
            
            # TSV导出
            tsv_path = output_path / "pubmed_articles.tsv"
            fields = ["xml_file", "index", "pmid", "doi", "title", "year", "authors", "abstract"]
            tsv_exporter = TsvExporter(fields=fields)
            tsv_exporter.export(all_articles, str(tsv_path))
            
            logger.info("处理完成，共处理 %d 篇文献", len(all_articles))
        else:
            logger.warning("未找到任何文章数据")
            
    except Exception as e:
        logger.error("处理过程中发生错误: %s", e)
        raise

if __name__ == "__main__":
    input_directory = "/data1/liubo_data/Paper_down/pubmed/xml"
    output_directory = "/data1/liubo_data/Paper_down/pubmed/paser"
    
    # 可以指定并行进程数，默认使用CPU核心数
    process_pubmed_files(
        input_directory, 
        output_directory,
        num_workers=4  # 指定使用4个进程，根据需要调整
    )