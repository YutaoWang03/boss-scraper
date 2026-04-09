"""
配置管理模块
"""

# 城市代码映射
CITY_CODES = {
    "杭州": "100010000",
    "北京": "100010000",
    "上海": "100010000",
    "广州": "100010000",
    "深圳": "100010000",
    "成都": "100010000",
    "武汉": "100010000",
    "西安": "100010000",
    "南京": "100010000",
    "苏州": "100010000",
    "重庆": "100010000",
    "天津": "100010000",
    "长沙": "100010000",
    "郑州": "100010000",
    "东莞": "100010000",
    "佛山": "100010000",
    "宁波": "100010000",
    "青岛": "100010000",
    "无锡": "100010000",
    "厦门": "100010000",
}

# 支持的输出格式
SUPPORTED_FORMATS = ['xlsx', 'csv', 'md', 'json']

# 风控配置
MIN_PAGE_DELAY = 5
MAX_PAGE_DELAY = 10
MIN_JOB_DELAY = 2
MAX_JOB_DELAY = 4

# 浏览器配置
DEFAULT_CHROME_PORT = 9222

# 默认配置
DEFAULT_CONFIG = {
    "keyword": None,
    "pages": None,
    "city": "杭州",
    "city_code": "100010000",
    "output_format": ["xlsx"],
    "output_dir": "./output",
    "data_dir": "./data",
    "chrome_port": 9222,
    "headless": False,
    "log_level": "INFO",
    "min_page_delay": 5,
    "max_page_delay": 10,
    "min_job_delay": 2,
    "max_job_delay": 4,
}


class Config:
    """配置类"""

    def __init__(self, **kwargs):
        """初始化配置"""
        for key, value in DEFAULT_CONFIG.items():
            setattr(self, key, kwargs.get(key, value))

        # 如果传了城市名，自动获取城市代码
        if hasattr(self, 'city') and self.city in CITY_CODES:
            self.city_code = CITY_CODES[self.city]

    def __repr__(self):
        return f"Config(keyword={self.keyword}, pages={self.pages}, city={self.city})"


def get_city_code(city_name: str) -> str:
    """获取城市代码"""
    return CITY_CODES.get(city_name, "100010000")


def list_cities() -> list:
    """获取支持的城市列表"""
    return list(CITY_CODES.keys())
