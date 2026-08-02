"""utils 模块单元测试."""

from src.utils import format_pct


def test_format_pct_typical():
    """正常百分比格式化."""
    assert format_pct(0.1234) == "12.34%"
    assert format_pct(0.5) == "50.00%"


def test_format_pct_zero_one():
    """边界值 0 和 1."""
    assert format_pct(0.0) == "0.00%"
    assert format_pct(1.0) == "100.00%"


def test_format_pct_custom_decimals():
    """自定义小数位数."""
    assert format_pct(0.1234, decimals=1) == "12.3%"
    assert format_pct(0.1234, decimals=4) == "12.3400%"
