"""
风控检测模块
检测登录页、验证码、账号异常等情况
"""


class RiskDetector:
    """风控检测器"""

    def __init__(self):
        """初始化检测器"""
        pass

    def check(self, page) -> dict:
        """
        检测风控提示

        Args:
            page: ChromiumPage 实例

        Returns:
            dict: {'is_risk': bool, 'message': str}
        """
        result = {'is_risk': False, 'message': ''}

        try:
            # 检测当前URL是否跳转到登录页
            current_url = page.url
            if 'login' in current_url.lower() or 'web/geek/login' in current_url.lower():
                result['is_risk'] = True
                result['message'] = '⚠️ 检测到登录页，需要登录账号'
                return result

            # 检测页面是否有验证码提示（只检测中文，精确匹配）
            page_html = page.html
            if '请输入验证码' in page_html or '输入验证码' in page_html:
                result['is_risk'] = True
                result['message'] = '⚠️ 检测到验证码挑战'
                return result

            # 检测是否有账号异常提示
            if '账号异常' in page_html or '账号限制' in page_html:
                result['is_risk'] = True
                result['message'] = '⚠️ 检测到账号异常提示'
                return result

            # 检测是否被限制访问
            if '访问频率过快' in page_html or '请稍后再试' in page_html:
                result['is_risk'] = True
                result['message'] = '⚠️ 检测到访问频率限制'
                return result

        except Exception as e:
            print(f"  ⚠️ 风控检测异常: {e}")

        return result

    def check_login_required(self, page) -> bool:
        """检测是否需要登录"""
        try:
            current_url = page.url
            return 'login' in current_url.lower() or 'web/geek/login' in current_url.lower()
        except:
            return False
