"""数据加载与预处理模块.

负责读取 CSV 数据、基础统计、缺失值检测与数据清洗.
"""

from pathlib import Path

import pandas as pd

# 项目数据目录
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data(filename: str) -> pd.DataFrame:
    """加载指定 CSV 文件.

    Args:
        filename: CSV 文件名(如 train.csv / test.csv).

    Returns:
        pd.DataFrame: 加载的数据.

    Raises:
        FileNotFoundError: 文件不存在时抛出.
    """
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"数据文件不存在: {filepath}")
    return pd.read_csv(filepath)


def get_column_info(df: pd.DataFrame) -> dict:
    """返回 DataFrame 各列的基础信息.

    Args:
        df: 输入 DataFrame.

    Returns:
        dict: 列名 → {dtype, missing_count, missing_pct, unique_count}.
    """
    info = {}
    for col in df.columns:
        missing = int(df[col].isna().sum())
        info[col] = {
            "dtype": str(df[col].dtype),
            "missing_count": missing,
            "missing_pct": round(missing / len(df) * 100, 2),
            "unique_count": int(df[col].nunique()),
        }
    return info


def get_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """返回数值列的汇总统计.

    Args:
        df: 输入 DataFrame.

    Returns:
        pd.DataFrame: 数值列的描述性统计.
    """
    return df.describe(include="all")


def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """返回类别型列名列表(object 或 category 类型).

    Args:
        df: 输入 DataFrame.

    Returns:
        list[str]: 类别列名.
    """
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """返回数值型列名列表.

    Args:
        df: 输入 DataFrame.

    Returns:
        list[str]: 数值列名.
    """
    return df.select_dtypes(include=["int64", "float64"]).columns.tolist()
