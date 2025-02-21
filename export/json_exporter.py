import json
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class JsonExporter:
    """JSON格式导出器"""
    
    def export(self, data: List[Dict[str, Any]], output_file: str):
        """
        将数据导出为JSON文件
        
        Args:
            data: 要导出的数据
            output_file: 输出文件路径
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Successfully exported data to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise 