"""
数据解析模块
解析页面元素，提取职位信息
"""

from typing import List, Dict
from src.utils.salary import decrypt_salary


class JobParser:
    """职位信息解析器"""

    def __init__(self):
        """初始化解析器"""
        pass

    def parse_job_card(self, job_element) -> Dict:
        """
        解析单个职位卡片

        Args:
            job_element: 职位卡片元素

        Returns:
            dict: 职位信息
        """
        try:
            # 基本信息
            job_name = self._get_text(job_element, '.job-name')
            salary = decrypt_salary(self._get_text(job_element, '.job-salary'))
            location = self._get_text(job_element, '.company-location')
            company = self._get_text(job_element, '.boss-name')
            tags = self._get_text(job_element, '.tag-list')

            # 解析城市和具体地址
            if '·' in location:
                city = location.split('·')[0].strip()
                detail_address = location.split('·')[1].strip() if len(location.split('·')) > 1 else ''
            else:
                city = location.strip()
                detail_address = ''

            # 获取职位链接
            job_url = ''
            try:
                job_name_elem = job_element('.job-name')
                href = job_name_elem.attr('href')
                if href:
                    job_url = f'{href}'
            except:
                pass

            return {
                '岗位名称': job_name,
                '薪资范围': salary,
                '工作城市': city,
                '具体地址': detail_address,
                '工作地点': location,
                '公司名称': company,
                '经验学历': tags,
                '职位链接': job_url,
                '职位描述': ''
            }

        except Exception as e:
            print(f"  ⚠️ 解析职位失败: {e}")
            return {}

    def parse_job_detail(self, page) -> str:
        """
        解析职位详情页

        Args:
            page: ChromiumPage 实例

        Returns:
            str: 职位描述
        """
        try:
            detail_box = page('.job-detail-box')
            if detail_box:
                full_text = detail_box.text
                pos_desc = full_text.find('职位描述')
                pos_app = full_text.find('去App')
                if pos_desc != -1 and pos_app != -1:
                    return full_text[pos_desc+4:pos_app].strip()
                return full_text
        except Exception as e:
            print(f"  ⚠️ 获取详情失败: {e}")
        return ''

    def parse_job_list(self, job_elements) -> List[Dict]:
        """
        解析职位列表

        Args:
            job_elements: 职位元素列表

        Returns:
            list: 职位信息列表
        """
        jobs = []
        for job_elem in job_elements:
            job_info = self.parse_job_card(job_elem)
            if job_info:
                jobs.append(job_info)
        return jobs

    def _get_text(self, element, selector: str) -> str:
        """获取元素文本"""
        try:
            elem = element(selector)
            return elem.text if elem else ''
        except:
            return ''
