"""
数据存储模块
支持多种格式的数据存储
"""

import os
import json
from datetime import datetime
from typing import List, Dict
import pandas as pd


class DataStorage:
    """数据存储器"""

    def __init__(self, output_dir: str = './output'):
        """
        初始化存储器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save(self, jobs: List[Dict], keyword: str, city: str, formats: List[str]):
        """
        保存数据

        Args:
            jobs: 职位信息列表
            keyword: 搜索关键词
            city: 城市
            formats: 输出格式列表
        """
        filename = self._generate_filename(keyword, city)

        for fmt in formats:
            filepath = os.path.join(self.output_dir, f'{filename}.{fmt}')
            if fmt == 'xlsx':
                self._save_excel(jobs, filepath)
            elif fmt == 'csv':
                self._save_csv(jobs, filepath)
            elif fmt == 'json':
                self._save_json(jobs, filepath)
            elif fmt == 'md':
                self._save_markdown(jobs, filepath)
            print(f"✅ 已保存: {filepath}")

    def _generate_filename(self, keyword: str, city: str) -> str:
        """生成文件名"""
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{keyword}_{city}_{date_str}"

    def _save_excel(self, jobs: List[Dict], filepath: str):
        """保存为 Excel"""
        df = pd.DataFrame(jobs)
        df.to_excel(filepath, index=False)

    def _save_csv(self, jobs: List[Dict], filepath: str):
        """保存为 CSV"""
        df = pd.DataFrame(jobs)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')

    def _save_json(self, jobs: List[Dict], filepath: str):
        """保存为 JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)

    def _save_markdown(self, jobs: List[Dict], filepath: str):
        """保存为 Markdown"""
        lines = ['# 职位信息\n']
        lines.append(f'共 {len(jobs)} 条记录\n\n')

        for i, job in enumerate(jobs, 1):
            lines.append(f'## {i}. {job.get("岗位名称", "")}\n')
            lines.append(f'- **薪资**: {job.get("薪资范围", "")}\n')
            lines.append(f'- **城市**: {job.get("工作城市", "")}\n')
            lines.append(f'- **公司**: {job.get("公司名称", "")}\n')
            lines.append(f'- **链接**: [查看]({job.get("职位链接", "")})\n')
            lines.append('\n')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
