"""模型训练模块.

负责构建预处理管道、训练分类模型、评估并保存模型.
"""

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data_loader import load_data

logger = logging.getLogger(__name__)

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
RANDOM_SEED = 42

# 预测时不可用的列(真实场景中无法提前获知)
EXCLUDE_COLS = ["duration", "id"]

# 目标列
TARGET_COL = "subscribe"


def prepare_features(
    df: pd.DataFrame,
    target_col: str = TARGET_COL,
    exclude_cols: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """分离特征与目标变量.

    Args:
        df: 原始数据.
        target_col: 目标列名.
        exclude_cols: 要从特征中排除的列.

    Returns:
        (X, y): 特征 DataFrame 与目标 Series.
    """
    if exclude_cols is None:
        exclude_cols = []
    drop_cols = [c for c in exclude_cols if c in df.columns]
    X = df.drop(columns=[target_col] + drop_cols, errors="ignore")
    y = (df[target_col] == "yes").astype(int)
    return X, y


def build_pipeline(numeric_cols: list[str], categorical_cols: list[str]) -> Pipeline:
    """构建预处理+分类 Pipeline.

    Args:
        numeric_cols: 数值列名.
        categorical_cols: 类别列名.

    Returns:
        sklearn Pipeline(ColumnTransformer → LogisticRegression).
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_cols,
            ),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=5000, random_state=RANDOM_SEED)),
        ]
    )


def train_model(
    pipeline: Pipeline, X_train: pd.DataFrame, y_train: pd.Series
) -> Pipeline:
    """训练模型.

    Args:
        pipeline: 未训练的 Pipeline.
        X_train: 训练特征.
        y_train: 训练目标.

    Returns:
        已训练的 Pipeline.
    """
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate_model(
    pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series
) -> dict[str, float]:
    """评估模型并返回指标.

    Args:
        pipeline: 已训练的 Pipeline.
        X_test: 测试特征.
        y_test: 测试目标.

    Returns:
        dict: {accuracy, precision, recall, f1, auc}.
    """
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1": round(f1_score(y_test, y_pred), 4),
        "auc": round(roc_auc_score(y_test, y_proba), 4),
    }


def save_model(pipeline: Pipeline, model_name: str = "model_pipeline") -> str:
    """保存模型到 models/ 目录.

    Args:
        pipeline: 已训练的 Pipeline.
        model_name: 模型文件名(不含扩展名).

    Returns:
        str: 保存的文件路径.
    """
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    path = MODEL_DIR / f"{model_name}.joblib"
    joblib.dump(pipeline, path)
    logger.info("模型已保存到 %s", path)
    return str(path)


def load_trained_model(model_name: str = "model_pipeline") -> Pipeline:
    """从 models/ 目录加载已训练模型.

    Args:
        model_name: 模型文件名(不含扩展名).

    Returns:
        Pipeline.

    Raises:
        FileNotFoundError: 模型文件不存在时抛出.
    """
    path = MODEL_DIR / f"{model_name}.joblib"
    if not path.exists():
        raise FileNotFoundError(f"模型文件不存在: {path}. 请先运行训练.")
    return joblib.load(path)


def run_full_training(train_csv: str = "train.csv", test_csv: str = "test.csv") -> dict:
    """端到端训练入口:加载数据 → 训练 → 评估 → 保存.

    使用 train.csv 拆分训练/验证集进行训练与评估;
    若 test.csv 包含目标列则额外评估,否则仅作预测用途说明.

    Args:
        train_csv: 训练数据文件名.
        test_csv: 测试数据文件名(可能无目标列).

    Returns:
        dict: 包含模型路径、评估指标、特征名称.
    """
    logger.info("开始训练流程...")

    train_df = load_data(train_csv)

    # 拆分训练集与验证集(train.csv 包含 subscribe 标签)
    train_df, val_df = train_test_split(
        train_df, test_size=0.2, random_state=RANDOM_SEED, stratify=train_df[TARGET_COL]
    )

    # ---- 对比: 含 duration vs 不含 duration ----
    for use_duration, label in [(False, "不含 duration"), (True, "含 duration")]:
        drop_cols = ["id"] if use_duration else EXCLUDE_COLS
        exclude = [c for c in drop_cols if c in train_df.columns]
        X_tr, y_tr = prepare_features(train_df, exclude_cols=exclude)
        X_va, y_va = prepare_features(val_df, exclude_cols=exclude)

        num_cols = X_tr.select_dtypes(include=["int64", "float64"]).columns.tolist()
        cat_cols = X_tr.select_dtypes(include=["object", "category"]).columns.tolist()

        pipe = build_pipeline(num_cols, cat_cols)
        pipe = train_model(pipe, X_tr, y_tr)
        m = evaluate_model(pipe, X_va, y_va)
        logger.info("模型评估(%s): %s", label, m)

        # 保存不含 duration 的模型作为默认模型
        if not use_duration:
            numeric_cols = num_cols
            categorical_cols = cat_cols
            pipeline = pipe
            metrics = m

    model_path = save_model(pipeline)

    return {
        "model_path": model_path,
        "metrics": metrics,
        "feature_names": numeric_cols + categorical_cols,
    }
