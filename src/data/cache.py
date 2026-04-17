"""
数据缓存模块
管理本地缓存数据，支持检查和读取
"""

import os
import glob
from typing import List, Optional
import pandas as pd


class DataCache:
    """数据缓存管理器"""

    def __init__(self, data_dir: str = './data'):
        """
        初始化缓存管理器

        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def find_cache(self, keyword: str, city: str) -> Optional[str]:
        """
        查找缓存数据

        Args:
            keyword: 搜索关键词
            city: 城市

        Returns:
            str: 缓存文件路径，如果不存在返回 None
        """
        pattern = os.path.join(self.data_dir, f'{keyword}_{city}_*.csv')
        files = glob.glob(pattern)

        if files:
            # 返回最新的文件
            latest = max(files, key=os.path.getmtime)
            return latest

        pattern = os.path.join(self.data_dir, f'{keyword}_{city}_*.xlsx')
        files = glob.glob(pattern)
        if files:
            latest = max(files, key=os.path.getmtime)
            return latest

        return None

    def load_cache(self, filepath: str) -> List[dict]:
        """
        加载缓存数据

        Args:
            filepath: 文件路径

        Returns:
            list: 职位信息列表
        """
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.json'):
            import json
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []

        return df.to_dict('records')

    def save_to_cache(self, jobs: List[dict], keyword: str, city: str) -> str:
        """
        保存数据到缓存

        Args:
            jobs: 职位信息列表
            keyword: 搜索关键词
            city: 城市

        Returns:
            str: 保存的文件路径
        """
        from datetime import datetime

        filename = f'{keyword}_{city}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = os.path.join(self.data_dir, filename)

        df = pd.DataFrame(jobs)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')

        return filepath

    def list_caches(self) -> List[str]:
        """
        列出所有缓存文件

        Returns:
            list: 缓存文件路径列表
        """
        patterns = ['*.csv', '*.xlsx', '*.json']
        files = []
        for pattern in patterns:
            files.extend(glob.glob(os.path.join(self.data_dir, pattern)))
        return sorted(files, key=os.path.getmtime, reverse=True)
