import csv
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TsvExporter:
    """TSV格式导出器"""
    
    def __init__(self, fields: List[str] = None):
        """
        初始化导出器
        
        Args:
            fields: 要导出的字段列表，如果为None则导出所有字段
        """
        self.fields = fields
    
    def export(self, data: List[Dict[str, Any]], output_file: str):
        """
        将数据导出为TSV文件
        
        Args:
            data: 要导出的数据
            output_file: 输出文件路径
        """
        try:
            if not data:
                logger.warning("No data to export")
                return
                
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 如果未指定字段，使用第一条数据的所有字段
            if not self.fields:
                self.fields = list(data[0].keys())
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='\t')
                
                # 写入表头
                writer.writerow(self.fields)
                
                # 写入数据
                for item in data:
                    row = [str(item.get(field, '')) for field in self.fields]
                    writer.writerow(row)
                    
            logger.info(f"Successfully exported data to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting to TSV: {e}")
            raise 