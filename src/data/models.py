"""
数据模型模块
定义职位信息的数据结构
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    """职位信息数据模型"""
    title: str = ''                    # 岗位名称
    salary: str = ''                    # 薪资范围
    salary_avg: Optional[int] = None     # 平均薪资
    city: str = ''                       # 工作城市
    address: str = ''                    # 具体地址
    full_location: str = ''              # 完整工作地点
    company: str = ''                   # 公司名称
    experience: str = ''                # 经验要求
    education: str = ''                 # 学历要求
    tags: str = ''                      # 职位标签
    skills: str = ''                   # 技能标签
    url: str = ''                       # 职位链接
    description: str = ''                # 职位描述

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            '岗位名称': self.title,
            '薪资范围': self.salary,
            '平均薪资': self.salary_avg,
            '工作城市': self.city,
            '具体地址': self.address,
            '工作地点': self.full_location,
            '公司名称': self.company,
            '经验要求': self.experience,
            '学历要求': self.education,
            '职位标签': self.tags,
            '技能标签': self.skills,
            '职位链接': self.url,
            '职位描述': self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Job':
        """从字典创建"""
        return cls(
            title=data.get('岗位名称', ''),
            salary=data.get('薪资范围', ''),
            salary_avg=data.get('平均薪资'),
            city=data.get('工作城市', ''),
            address=data.get('具体地址', ''),
            full_location=data.get('工作地点', ''),
            company=data.get('公司名称', ''),
            experience=data.get('经验要求', ''),
            education=data.get('学历要求', ''),
            tags=data.get('职位标签', ''),
            skills=data.get('技能标签', ''),
            url=data.get('职位链接', ''),
            description=data.get('职位描述', ''),
        )
