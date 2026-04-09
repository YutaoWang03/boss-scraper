"""
爬虫入口模块
整合所有模块，提供统一的爬虫接口
"""

from typing import List, Dict, Optional
from time import sleep
import random

from src.core.browser import BrowserManager
from src.core.detector import RiskDetector
from src.core.parser import JobParser
from src.data.storage import DataStorage
from src.data.cache import DataCache


class BossScraper:
    """Boss直聘爬虫"""

    def __init__(self, config: dict):
        """
        初始化爬虫

        Args:
            config: 配置字典
        """
        self.config = config
        self.browser = BrowserManager(config.get('chrome_port', 9222))
        self.detector = RiskDetector()
        self.parser = JobParser()
        self.storage = DataStorage(config.get('output_dir', './output'))
        self.cache = DataCache(config.get('data_dir', './data'))
        self.page = None

    def scrape(self, keyword: str, pages: int, city: str, city_code: str) -> List[Dict]:
        """
        执行爬取

        Args:
            keyword: 搜索关键词
            pages: 爬取页数
            city: 城市名称
            city_code: 城市代码

        Returns:
            list: 职位信息列表
        """
        print("正在连接Chrome...")
        self.page = self.browser.connect()
        print("Chrome连接成功!")

        jobs = []

        for page in range(pages):
            print(f'\n=== 正在采集第 {page + 1}/{pages} 页 ===')

            # 访问搜索页
            url = f'https://www.zhipin.com/web/geek/job?query={keyword}&city={city_code}'
            self.page.get(url)

            # 随机延迟
            self._random_delay(2, 4)

            # 检测风控
            risk = self.detector.check(self.page)
            if risk['is_risk']:
                print(f"\n{risk['message']}")
                print("💾 保存已有数据并退出...")
                break

            # 随机滚动
            self._random_scroll()

            # 获取职位列表
            job_elements = self.page.eles('css:.job-card-wrap')
            print(f"找到 {len(job_elements)} 个职位")

            for i, job_elem in enumerate(job_elements):
                job_info = self.parser.parse_job_card(job_elem)

                # 点击获取详情
                try:
                    job_elem.click()
                    self._random_delay(1, 2.5)
                    job_info['职位描述'] = self.parser.parse_job_detail(self.page)
                except:
                    pass

                print(f"  {i+1}. {job_info.get('岗位名称', '')} | {job_info.get('薪资范围', '')} | {job_info.get('公司名称', '')}")
                jobs.append(job_info)

                # 职位间延迟
                if i < len(job_elements) - 1:
                    self._random_delay(2, 4)

            # 页面间延迟
            if page < pages - 1:
                print(f"\n📄 页面完成，开始随机等待...")
                self._random_delay(5, 10)

        # 保存到缓存
        if jobs:
            self.cache.save_to_cache(jobs, keyword, city)

        return jobs

    def run(self, keyword: str, pages: int, city: str, city_code: str,
            formats: List[str], use_cache: bool = False, force: bool = False) -> List[Dict]:
        """
        运行爬虫

        Args:
            keyword: 搜索关键词
            pages: 爬取页数
            city: 城市名称
            city_code: 城市代码
            formats: 输出格式
            use_cache: 是否使用缓存
            force: 是否强制重新抓取

        Returns:
            list: 职位信息列表
        """
        # 检查缓存
        if not force:
            cache_file = self.cache.find_cache(keyword, city)
            if cache_file:
                print(f"找到缓存文件: {cache_file}")
                print("选项: 1. 使用缓存  2. 重新抓取  3. 取消")
                choice = input("请选择: ").strip()

                if choice == '1':
                    jobs = self.cache.load_cache(cache_file)
                    print(f"已加载 {len(jobs)} 条缓存数据")
                    return jobs
                elif choice == '3':
                    return []

        # 执行爬取
        jobs = self.scrape(keyword, pages, city, city_code)

        # 保存数据
        if jobs:
            self.storage.save(jobs, keyword, city, formats)
            print(f"\n📊 共获取 {len(jobs)} 条职位信息")

        return jobs

    def _random_delay(self, min_sec: float, max_sec: float):
        """随机延迟"""
        delay = random.uniform(min_sec, max_sec)
        print(f"  ⏳ 等待 {delay:.1f} 秒...")
        sleep(delay)

    def _random_scroll(self):
        """随机滚动"""
        from time import sleep
        for _ in range(random.randint(1, 2)):
            self.page.scroll.to_bottom()
            sleep(random.uniform(0.5, 1.5))
