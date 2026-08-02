"""data_loader 模块单元测试."""

import pandas as pd
import pytest

from src.data_loader import (
    get_categorical_columns,
    get_column_info,
    get_numeric_columns,
    get_summary_stats,
    load_data,
)


@pytest.fixture
def sample_df():
    """构造测试用 DataFrame."""
    return pd.DataFrame(
        {
            "age": [30, 45, 28, 50],
            "job": ["admin.", "services", "blue-collar", "entrepreneur"],
            "salary": [50000.0, None, 62000.0, 78000.0],
            "subscribe": ["no", "yes", "no", "yes"],
        }
    )


def test_load_data_returns_dataframe():
    """正常加载 CSV 返回 DataFrame."""
    df = load_data("train.csv")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "subscribe" in df.columns


def test_load_data_file_not_found():
    """不存在的文件抛出 FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="数据文件不存在"):
        load_data("nonexistent.csv")


def test_get_column_info_structure(sample_df):
    """列信息应包含正确的键与统计."""
    info = get_column_info(sample_df)
    assert "age" in info
    assert info["age"]["dtype"] in ("int64", "int32")
    assert info["salary"]["missing_count"] == 1
    assert info["salary"]["missing_pct"] == 25.0


def test_get_summary_stats(sample_df):
    """汇总统计应返回 DataFrame."""
    stats = get_summary_stats(sample_df)
    assert isinstance(stats, pd.DataFrame)


def test_get_categorical_columns(sample_df):
    """应正确识别类别列."""
    cat_cols = get_categorical_columns(sample_df)
    assert "job" in cat_cols
    assert "subscribe" in cat_cols
    assert "age" not in cat_cols


def test_get_numeric_columns(sample_df):
    """应正确识别数值列."""
    num_cols = get_numeric_columns(sample_df)
    assert "age" in num_cols
    assert "salary" in num_cols
    assert "job" not in num_cols
