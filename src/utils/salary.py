"""
薪资解密模块
Boss直聘使用自定义字体加密薪资数据
"""

# Boss直聘薪资字体映射（Unicode -> 数字）
SALARY_FONT_MAP = {
    '\ue030': '0', '\ue031': '0', '\ue032': '1', '\ue033': '2',
    '\ue034': '3', '\ue035': '4', '\ue036': '5', '\ue037': '6',
    '\ue038': '7', '\ue039': '9', '\ue03a': '8', '\ue03b': '3',
    '\ue03c': '5', '\ue03d': '1', '\ue03e': '2', '\ue03f': '3',
    '\ue040': '4', '\ue041': '5', '\ue042': '6', '\ue043': '7',
    '\ue044': '8', '\ue045': '9', '\ue046': '0',
    '\ue026': 'K', '\ue027': 'k', '\ue028': '薪', '\ue029': '元',
    '\ue02a': '/', '\ue02b': '-',
}


def decrypt_salary(encrypted_text: str) -> str:
    """
    解密薪资文本

    Args:
        encrypted_text: 加密的薪资文本

    Returns:
        解密后的薪资文本
    """
    if not encrypted_text:
        return ''
    result = encrypted_text
    for char, digit in SALARY_FONT_MAP.items():
        result = result.replace(char, digit)
    return result


def parse_salary(salary_str: str) -> tuple:
    """
    解析薪资字符串，返回(最低, 最高, 平均月薪)

    Args:
        salary_str: 薪资字符串，如 "20-40K·15薪" 或 "200-300元/天"

    Returns:
        (最低薪资, 最高薪资, 月薪) 元组
    """
    import re

    # 处理加密后的薪资
    salary_str = decrypt_salary(salary_str)

    # 尝试匹配 K/月薪 格式
    match = re.search(r'(\d+)[-–](\d+)[kK](?:·(\d+)薪)?', salary_str)
    if match:
        low = int(match.group(1)) * 1000
        high = int(match.group(2)) * 1000
        months = int(match.group(3)) if match.group(3) else 12
        avg = (low + high) // 2
        return (low, high, avg, months)

    # 尝试匹配 元/天 格式
    match = re.search(r'(\d+)[-–](\d+)元/天', salary_str)
    if match:
        low = int(match.group(1)) * 22  # 按22天工作日估算
        high = int(match.group(2)) * 22
        avg = (low + high) // 2
        return (low, high, avg, 22)

    # 尝试匹配 元/月 格式
    match = re.search(r'(\d+)[-–](\d+)元/月', salary_str)
    if match:
        low = int(match.group(1))
        high = int(match.group(2))
        avg = (low + high) // 2
        return (low, high, avg, 1)

    return (0, 0, 0, 0)
