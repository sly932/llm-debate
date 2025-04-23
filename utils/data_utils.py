"""
数据工具模块

此模块提供了处理数据的工具函数。
"""

import json
import os
from typing import Dict, List, Optional, Any

class DataManager:
    """数据管理类，用于处理数据相关操作"""
    def __init__(self, data_dir: str = "data"):
        """
        初始化数据管理器
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    def save_debate(self, debate_id: str, debate_data: Dict[str, Any]) -> str:
        """
        保存辩论数据
        Args:
            debate_id: 辩论ID
            debate_data: 辩论数据
        Returns:
            str: 保存的文件路径
        """
        file_path = os.path.join(self.data_dir, f"{debate_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(debate_data, f, ensure_ascii=False, indent=2)
        return file_path
    def load_debate(self, debate_id: str) -> Optional[Dict[str, Any]]:
        """
        加载辩论数据
        Args:
            debate_id: 辩论ID
        Returns:
            Optional[Dict[str, Any]]: 辩论数据，如果不存在则返回None
        """
        file_path = os.path.join(self.data_dir, f"{debate_id}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    def list_debates(self) -> List[str]:
        """
        列出所有辩论
        Returns:
            List[str]: 辩论ID列表
        """
        if not os.path.exists(self.data_dir):
            return []
        return [
            f.split(".")[0] for f in os.listdir(self.data_dir)
            if f.endswith(".json")
        ]
    def delete_debate(self, debate_id: str) -> bool:
        """
        删除辩论数据
        Args:
            debate_id: 辩论ID
        Returns:
            bool: 是否成功删除
        """
        file_path = os.path.join(self.data_dir, f"{debate_id}.json")
        if not os.path.exists(file_path):
            return False
        os.remove(file_path)
        return True

