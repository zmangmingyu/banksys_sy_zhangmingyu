"""公共工具函数."""


def format_pct(value: float, decimals: int = 2) -> str:
    """将小数格式化为百分比字符串.

    Args:
        value: 小数值,如 0.1234.
        decimals: 小数位数.

    Returns:
        str: 如 "12.34%".
    """
    return f"{value * 100:.{decimals}f}%"
