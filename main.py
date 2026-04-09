#!/usr/bin/env python3
"""
Boss直聘爬虫 - CLI 入口
"""

import argparse
import sys
import os
from datetime import datetime

# 尝试导入 readchar（用于键盘交互）
try:
    import readchar
    HAS_READCHAR = True
except Exception:
    HAS_READCHAR = False

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import get_city_code
from src.api.scraper import BossScraper
from src.analytics.report import run_analysis


def print_banner():
    """打印欢迎信息"""
    print("=" * 50)
    print("Boss直聘爬虫 v1.0")
    print("=" * 50)


# def clear_menu(num_lines):
#     """清除指定行数，回到菜单开头"""
#     for _ in range(num_lines):
#         print("\033[A\033[K", end="")
#     print("\r", end="")

def clear_menu(n):
    """向上移动光标并清空这 n 行"""
    for _ in range(n):
        sys.stdout.write('\033[1A')  # 光标向上移动 1 行
        sys.stdout.write('\033[2K')  # 清除当前行
        sys.stdout.write('\r')       # 光标回到行首
    sys.stdout.flush()


# def get_choice(options, prompt="请选择"):
#     """单选交互（方向键选择，回车确认）"""
#     if not HAS_READCHAR:
#         return _simple_choice(options, prompt)

#     current = 0
#     num_lines = len(options) + 1  # 选项行数 + 提示行

#     # 首次显示
#     print(f"\n{prompt}（↑/↓ 选择，回车确认，Esc 退出）:")
#     for i, opt in enumerate(options):
#         marker = "▶" if i == current else " "
#         color = "\033[32m" if i == current else ""
#         reset = "\033[0m" if i == current else ""
#         print(f"  {color}{marker}{reset} {opt}")

#     while True:
#         # 读取按键
#         try:
#             key = readchar.readkey()
#         except:
#             return _simple_choice(options, prompt)

#         if key == readchar.key.UP:
#             clear_menu(num_lines)
#             current = (current - 1) % len(options)
#             print(f"{prompt}（↑/↓ 选择，回车确认，Esc 退出）:")
#             for i, opt in enumerate(options):
#                 marker = "▶" if i == current else " "
#                 color = "\033[32m" if i == current else ""
#                 reset = "\033[0m" if i == current else ""
#                 print(f"  {color}{marker}{reset} {opt}")
#         elif key == readchar.key.DOWN:
#             clear_menu(num_lines)
#             current = (current + 1) % len(options)
#             print(f"{prompt}（↑/↓ 选择，回车确认，Esc 退出）:")
#             for i, opt in enumerate(options):
#                 marker = "▶" if i == current else " "
#                 color = "\033[32m" if i == current else ""
#                 reset = "\033[0m" if i == current else ""
#                 print(f"  {color}{marker}{reset} {opt}")
#         elif key == readchar.key.CTRL_C or key == '\x1b':  # Esc
#             raise KeyboardInterrupt
#         elif key in (readchar.key.ENTER, '\r', '\n'):  # Enter
#             clear_menu(num_lines)
#             return current + 1



# def get_multi_choice(options, prompt="请选择"):
#     """多选交互（空格键切换选项，回车确认选择）"""
#     if not HAS_READCHAR:
#         return _simple_multi_choice(options, prompt)

#     selected = [False] * len(options)
#     current = 0
#     num_lines = len(options) + 1  # 选项行数 + 提示行

#     # 首次显示
#     print(f"\n{prompt}（↑/↓ 移动，空格切换，回车确认）:")
#     for i, opt in enumerate(options):
#         if i == current:
#             prefix = "✓" if selected[i] else "▶"
#             print(f"  \033[32m{prefix}\033[0m {opt}")
#         else:
#             prefix = "✓" if selected[i] else " "
#             print(f"   {prefix} {opt}")

#     while True:
#         try:
#             key = readchar.readkey()
#         except:
#             return _simple_multi_choice(options, prompt)

#         if key == readchar.key.UP:
#             clear_menu(num_lines)
#             current = (current - 1) % len(options)
#             print(f"{prompt}（↑/↓ 移动，空格切换，回车确认）:")
#             for i, opt in enumerate(options):
#                 if i == current:
#                     prefix = "✓" if selected[i] else "▶"
#                     print(f"  \033[32m{prefix}\033[0m {opt}")
#                 else:
#                     prefix = "✓" if selected[i] else " "
#                     print(f"   {prefix} {opt}")
#         elif key == readchar.key.DOWN:
#             clear_menu(num_lines)
#             current = (current + 1) % len(options)
#             print(f"{prompt}（↑/↓ 移动，空格切换，回车确认）:")
#             for i, opt in enumerate(options):
#                 if i == current:
#                     prefix = "✓" if selected[i] else "▶"
#                     print(f"  \033[32m{prefix}\033[0m {opt}")
#                 else:
#                     prefix = "✓" if selected[i] else " "
#                     print(f"   {prefix} {opt}")
#         elif key == ' ':
#             selected[current] = not selected[current]
#             # 刷新整个菜单
#             clear_menu(num_lines)
#             print(f"{prompt}（↑/↓ 移动，空格切换，回车确认）:")
#             for i, opt in enumerate(options):
#                 if i == current:
#                     prefix = "✓" if selected[i] else "▶"
#                     print(f"  \033[32m{prefix}\033[0m {opt}")
#                 else:
#                     prefix = "✓" if selected[i] else " "
#                     print(f"   {prefix} {opt}")
#         elif key == readchar.key.CTRL_C or key == '\x1b':
#             raise KeyboardInterrupt
#         elif key in (readchar.key.ENTER, '\r', '\n'):
#             clear_menu(num_lines)
#             result = [options[i] for i in range(len(options)) if selected[i]]
#             if result:
#                 return result
#             print("请至少选择一个选项")

import sys

# 辅助常量
COLOR_GREEN = "\033[32m"
COLOR_BRIGHT = "\033[1;37;42m" # 加粗白字绿底
RESET = "\033[0m"

def render_menu(options, current_idx, selected_mask, prompt, is_multi=False):
    """
    统一渲染函数
    :param selected_mask: 布尔列表，记录哪些被勾选了
    """
    if prompt:
        print(f"\r{prompt}:")  # \r 回到行首
    for i, opt in enumerate(options):
        is_current = (i == current_idx)
        
        # 1. 确定前缀符号
        if is_multi:
            checkbox = " [x] " if selected_mask[i] else " [ ] "
            marker = " > " if is_current else "   "
            prefix = marker + checkbox
        else:
            prefix = " > " if is_current else "   "

        # 2. 突出显示效果：如果是当前选中的行，使用反色或高亮背景
        if is_current:
            # 这里使用了绿色加粗，你也可以换成 \033[7m 实现反白突出
            line = f"{COLOR_BRIGHT}{prefix}{opt}{RESET}"
        else:
            line = f" {prefix}{opt} "
            
        print(f"  {line}")


def get_choice(options, prompt="请选择"):
    """
    单选交互（方向键选择，回车确认）
    """
    if not HAS_READCHAR:
        return _simple_choice(options, prompt)

    current = 0
    num_lines = len(options) + (1 if prompt else 0)  # 选项行数 + 可选提示行

    # 隐藏光标
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            # 渲染菜单：selected_mask 传 None 或全 False 即可，因为单选不需要勾选框
            render_menu(options, current, None, prompt, is_multi=False)

            key = readchar.readkey()

            if key == readchar.key.UP:
                current = (current - 1) % len(options)
            elif key == readchar.key.DOWN:
                current = (current + 1) % len(options)
            elif key == '\x1b':  # Esc 退出
                sys.stdout.write("\033[?25h")
                raise KeyboardInterrupt
            elif key in (readchar.key.ENTER, '\r', '\n'):
                # 选完即走，清理屏幕后返回结果
                clear_menu(num_lines)
                sys.stdout.write("\033[?25h")
                return current + 1 # 返回 1-based 索引，或者直接返回 options[current]

            # 准备重绘
            clear_menu(num_lines)

    except Exception as e:
        sys.stdout.write("\033[?25h") # 发生异常也要恢复光标
        raise e
    
def get_multi_choice(options, prompt="请选择选项"):
    if not HAS_READCHAR:
        return _simple_multi_choice(options, prompt)

    current = 0
    selected = [False] * len(options)
    num_lines = len(options) + (1 if prompt else 0)

    # 隐藏光标（让交互看起来更专业）
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            # 渲染当前状态
            render_menu(options, current, selected, prompt, is_multi=True)
            
            key = readchar.readkey()

            if key == readchar.key.UP:
                current = (current - 1) % len(options)
            elif key == readchar.key.DOWN:
                current = (current + 1) % len(options)
            elif key == ' ': # 空格键标记
                selected[current] = not selected[current]
            elif key in (readchar.key.ENTER, '\r', '\n'):
                if any(selected):
                    break # 至少选一个才退出
            elif key == '\x1b': # Esc
                sys.stdout.write("\033[?25h") # 显示光标
                raise KeyboardInterrupt

            # 清除之前的菜单，准备重绘
            clear_menu(num_lines)
            
        # 最终清理并返回
        clear_menu(num_lines)
        sys.stdout.write("\033[?25h")
        return [opt for i, opt in enumerate(options) if selected[i]]

    except Exception as e:
        sys.stdout.write("\033[?25h")
        raise e

def _simple_choice(options, prompt="请选择"):
    """简单版本（数字选择）"""
    while True:
        if prompt:
            print(f"\n{prompt}:")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")

        choice = input(f"\n请选择 [1-{len(options)}]: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print("输入无效，请重新选择")


def _simple_multi_choice(options, prompt="请选择"):
    """多选简单版本（数字逗号分隔）"""
    while True:
        print(f"\n{prompt}（空格切换，回车确认）:")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")

        choice = input(f"\n请选择（可多选，如 1,2,3）: ").strip()
        if choice:
            try:
                indices = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]
                if all(1 <= i <= len(options) for i in indices):
                    return [options[i-1] for i in indices]
            except:
                pass
        print("输入无效")


def interactive_mode():
    """交互式模式"""
    print("\n" + "=" * 50)
    print("Boss直聘爬虫 - 交互式向导")
    print("=" * 50)

    # 步骤1：选择操作（单选）
    print("\n【步骤1】请选择操作:")
    mode_options = ["数据抓取", "数据分析（离线）", "抓取并分析"]
    mode = get_choice(mode_options, "")
    print(f"  ✓ 已选择: {mode_options[mode - 1]}")

    if mode == 2:
        print("\n请输入已导出的职位数据文件路径（.csv 或 .json）:")
        path = input(" > 路径: ").strip().strip('"').strip("'")
        if not path:
            print("路径不能为空")
            return None
        ap = os.path.abspath(path)
        if not os.path.isfile(ap):
            print(f"文件不存在: {ap}")
            return None
        try:
            run_analysis(ap, report_dir=None)
        except (FileNotFoundError, ValueError) as e:
            print(f"❌ 分析失败: {e}")
        except Exception as e:
            print(f"❌ 分析失败: {e}")
        return None

    analyze_after = mode == 3

    # 步骤2：输入搜索关键词
    print("\n【步骤2】请输入搜索关键词:")
    keyword = input(" > 关键词: ").strip()
    if not keyword:
        print("关键词不能为空")
        return None
    print(f"  ✓ 关键词: {keyword}")

    # 步骤3：选择页数
    print("\n【步骤3】请选择爬取页数:")
    page_options = ["1页 (约30条)", "2页 (约60条)", "3页 (约90条)", "5页 (约150条)", "10页 (约300条)"]
    pages_map = {"1页 (约30条)": 1, "2页 (约60条)": 2, "3页 (约90条)": 3, "5页 (约150条)": 5, "10页 (约300条)": 10}
    page_label = page_options[get_choice(page_options, "") - 1]
    pages = pages_map[page_label]
    print(f"  ✓ 已选择: {page_label}")

    # 步骤4：选择城市
    print("\n【步骤4】请选择城市:")
    city_options = ["杭州", "北京", "上海", "广州", "深圳", "成都", "武汉", "南京", "苏州", "重庆", "自定义"]
    city_result = get_multi_choice(city_options, "")
    print(f"  ✓ 已选择: {', '.join(city_result)}")

    if "自定义" in city_result:
        city = input("请输入城市名称: ").strip()
    else:
        city = city_result[0]

    city_code = get_city_code(city)

    # 步骤5：选择输出格式（多选）
    print("\n【步骤5】请选择输出格式:")
    fmt_options = ["Excel (.xlsx)", "CSV (.csv)", "Markdown (.md)", "JSON (.json)"]
    fmt_result = get_multi_choice(fmt_options, "")
    print(f"  ✓ 已选择: {', '.join(fmt_result)}")

    format_map = {"Excel (.xlsx)": "xlsx", "CSV (.csv)": "csv", "Markdown (.md)": "md", "JSON (.json)": "json"}
    selected_formats = [format_map[f] for f in fmt_result]

    # 步骤6：数据选项
    print("\n【步骤6】请选择数据选项:")
    cache_choice = get_choice(["使用已有缓存数据", "重新抓取新数据"], "")
    use_cache = (cache_choice == 1)
    print(f"  ✓ 已选择: {'使用已有缓存数据' if use_cache else '重新抓取新数据'}")

    return {
        'keyword': keyword,
        'pages': pages,
        'city': city,
        'city_code': city_code,
        'formats': selected_formats,
        'use_cache': use_cache,
        'analyze_after': analyze_after,
    }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Boss直聘职位爬虫')
    parser.add_argument('-k', '--keyword', type=str, help='搜索关键词')
    parser.add_argument('-p', '--pages', type=int, default=1, help='爬取页数')
    parser.add_argument('-c', '--city', type=str, default='杭州', help='城市')
    parser.add_argument('--format', type=str, help='输出格式(xlsx,csv,md,json)，逗号分隔')
    parser.add_argument('-o', '--output', type=str, default='./output', help='输出目录')
    parser.add_argument('--data-dir', type=str, default='./data', help='数据目录')
    parser.add_argument('--chrome-port', type=int, default=9222, help='Chrome调试端口')
    parser.add_argument('--force', action='store_true', help='强制重新抓取')
    parser.add_argument('-i', '--interactive', action='store_true', help='交互式模式')
    parser.add_argument('--analyze', type=str, metavar='PATH', help='仅离线分析 CSV/JSON，不启动爬虫')
    parser.add_argument('--report-dir', type=str, default=None, help='分析报告输出根目录（默认 output/reports）')

    args = parser.parse_args()

    print_banner()

    if args.analyze:
        try:
            run_analysis(args.analyze, report_dir=args.report_dir)
        except (FileNotFoundError, ValueError) as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ 分析失败: {e}")
        return

    # 交互式模式（无关键词时进入向导；有 -k 时仅当 -i 才进入）
    if args.interactive or (not args.keyword):
        config = interactive_mode()
        if not config:
            return
    else:
        config = {
            'keyword': args.keyword,
            'pages': args.pages,
            'city': args.city,
            'city_code': get_city_code(args.city),
            'formats': args.format.split(',') if args.format else ['xlsx'],
            'output_dir': args.output,
            'data_dir': args.data_dir,
            'chrome_port': args.chrome_port,
            'use_cache': False,
            'analyze_after': False,
        }

    # 打印配置
    print("\n" + "=" * 50)
    print("⚠️  风控提示")
    print("=" * 50)
    print("• 请使用独立账号爬取，避免主账号被封")
    print("• 建议每天爬取不超过 200-300 条")
    print("• 适当休息，避免 24 小时连续爬取")
    print("=" * 50)
    print(f"\n关键词: {config['keyword']}")
    print(f"页数: {config['pages']}")
    print(f"城市: {config['city']}")
    print(f"输出格式: {config['formats']}")
    print("=" * 50 + "\n")

    # 运行爬虫
    scraper = BossScraper(config)
    jobs = scraper.run(
        keyword=config['keyword'],
        pages=config['pages'],
        city=config['city'],
        city_code=config['city_code'],
        formats=config['formats'],
        use_cache=config.get('use_cache', False),
        force=args.force,
    )

    if not jobs:
        print("❌ 未获取到任何职位信息")
        return

    if config.get('analyze_after'):
        bn = f"{config['keyword']}_{config['city']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            run_analysis(jobs, report_dir=args.report_dir, basename=bn)
        except ValueError as e:
            print(f"❌ 分析失败: {e}")


if __name__ == '__main__':
    main()
