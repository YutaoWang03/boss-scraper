"""
浏览器管理模块
基于 DrissionPage 管理 Chrome 浏览器
"""

from DrissionPage import ChromiumPage, ChromiumOptions


class BrowserManager:
    """浏览器管理器"""

    def __init__(self, port: int = 9222):
        """
        初始化浏览器管理器

        Args:
            port: Chrome 调试端口
        """
        self.port = port
        self.page = None

    def connect(self) -> ChromiumPage:
        """
        连接已启动的 Chrome 浏览器

        Returns:
            ChromiumPage 实例
        """
        self.page = ChromiumPage(f'127.0.0.1:{self.port}')
        return self.page

    def auto_start(self, headless: bool = False) -> ChromiumPage:
        """
        自动启动 Chrome

        Args:
            headless: 是否无头模式

        Returns:
            ChromiumPage 实例
        """
        options = ChromiumOptions()
        options.set_argument('--disable-blink-features=AutomationControlled')
        options.set_argument('--no-sandbox')
        options.set_argument('--disable-dev-shm-usage')

        if headless:
            options.set_argument('--headless=new')

        options.set_argument('--user-data-dir=/tmp/chrome-user-data')
        self.page = ChromiumPage(options)
        return self.page

    def get_page(self) -> ChromiumPage:
        """获取页面实例"""
        return self.page

    def close(self):
        """关闭浏览器（可选）"""
        if self.page:
            try:
                self.page.quit()
            except:
                pass
