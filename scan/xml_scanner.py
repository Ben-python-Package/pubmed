import os
from pathlib import Path
from typing import List
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scan_xml_files(directory: str) -> List[str]:
    """
    扫描指定目录及其子目录下的所有XML文件
    
    Args:
        directory (str): 要扫描的目录路径
        
    Returns:
        List[str]: 包含所有XML文件完整路径的列表
        
    Raises:
        FileNotFoundError: 如果指定目录不存在
        PermissionError: 如果没有访问目录的权限
    """
    try:
        # 将输入路径转换为Path对象
        dir_path = Path(directory)
        
        # 检查目录是否存在
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        # 检查是否为目录
        if not dir_path.is_dir():
            raise NotADirectoryError(f"指定路径不是目录: {directory}")
            
        xml_files = []
        
        logger.info(f"开始扫描目录: {directory}")
        
        # 使用rglob递归遍历所有文件
        for file_path in dir_path.rglob("*.xml"):
            try:
                if file_path.is_file():
                    xml_files.append(str(file_path.absolute()))
                    logger.debug(f"找到XML文件: {file_path}")
            except PermissionError as e:
                logger.warning(f"无法访问文件 {file_path}: {e}")
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时发生错误: {e}")
                
        logger.info(f"扫描完成，共找到 {len(xml_files)} 个XML文件")
        return xml_files
        
    except PermissionError as e:
        logger.error(f"无法访问目录 {directory}: {e}")
        raise
    except Exception as e:
        logger.error(f"扫描目录时发生错误: {e}")
        raise

if __name__ == "__main__":
    # 示例用法
    try:
        test_dir = "."  # 当前目录
        xml_files = scan_xml_files(test_dir)
        print("\n找到的XML文件:")
        for xml_file in xml_files:
            print(f"- {xml_file}")
    except Exception as e:
        print(f"错误: {e}") 