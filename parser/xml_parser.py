import xml.etree.ElementTree as ET
from typing import Dict, List, Any
from pathlib import Path
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

class PubmedParser:
    """PubMed XML文件解析器"""
    
    def parse_file(self, file_path: str, show_progress: bool = False) -> List[Dict[str, Any]]:
        """
        解析PubMed XML文件
        
        Args:
            file_path: XML文件路径
            show_progress: 是否显示解析进度
            
        Returns:
            解析后的文献数据列表
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            articles = []
            
            # 获取文章总数
            all_articles = root.findall(".//PubmedArticle")
            total_articles = len(all_articles)
            
            # 创建进度条
            if show_progress:
                pbar = tqdm(total=total_articles, 
                          desc="解析文献", 
                          position=1, 
                          leave=False)
                pbar.update(1)

            
            for index, article in enumerate(all_articles, 1):
                parsed_article = self._parse_article(index, article)
                parsed_article["xml_file"] = file_path.split("/")[-1]
                articles.append(parsed_article)
                
                if show_progress:
                    pbar.update(1)
            
            if show_progress:
                pbar.close()
                
            return articles
            
        except Exception as e:
            logger.error("Error parsing file %s: %s", file_path, e)
            raise

    def _parse_article(self, index: int, article: ET.Element) -> Dict[str, Any]:
        """解析单篇文献"""
        # 获取PMID
        doi = ""
        pmid = article.find(".//PMID").text
        # 获取文章标题
        title = article.find(".//ArticleTitle")
        title = title.text if title is not None else ""
        # 获取摘要
        abstract_parts = article.findall(".//Abstract/AbstractText")
        abstract = " ".join(part.text for part in abstract_parts if part.text)
        for id_list in article.findall(".//ArticleId"):
            if id_list.attrib["IdType"] == "doi":
                doi = id_list.text

        # 获取作者列表
        authors = []
        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            if last_name is not None and fore_name is not None:
                authors.append(f"{fore_name.text} {last_name.text}")
        # 获取发表日期
        pub_date = article.find(".//PubDate")
        year = pub_date.find("Year")
        year = year.text if year is not None else ""
        return {
            "index": index,
            "title": title,
            "pmid": pmid,
            "doi": doi,
            "abstract": abstract,
            "authors": authors,
            "year": year
        }
