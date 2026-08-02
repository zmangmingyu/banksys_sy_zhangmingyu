"""model_trainer 模块单元测试."""

import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from src.model_trainer import (
    build_pipeline,
    evaluate_model,
    load_trained_model,
    prepare_features,
    save_model,
    train_model,
)


@pytest.fixture
def sample_train_df():
    """合成训练数据."""
    n = 100
    np.random.seed(42)
    return pd.DataFrame(
        {
            "age": np.random.randint(20, 65, n),
            "job": np.random.choice(["admin.", "blue-collar", "services"], n),
            "salary": np.random.normal(50000, 15000, n),
            "subscribe": np.random.choice(["no", "yes"], n, p=[0.7, 0.3]),
            "duration": np.random.randint(0, 5000, n),
        }
    )


@pytest.fixture
def sample_test_df():
    """合成测试数据."""
    n = 40
    np.random.seed(99)
    return pd.DataFrame(
        {
            "age": np.random.randint(20, 65, n),
            "job": np.random.choice(["admin.", "blue-collar", "services"], n),
            "salary": np.random.normal(50000, 15000, n),
            "subscribe": np.random.choice(["no", "yes"], n, p=[0.7, 0.3]),
            "duration": np.random.randint(0, 5000, n),
        }
    )


def test_prepare_features_excludes_duration(sample_train_df):
    """特征准备时应排除 duration 列."""
    X, y = prepare_features(sample_train_df, exclude_cols=["duration"])
    assert "duration" not in X.columns
    assert "subscribe" not in X.columns
    assert len(y) == len(sample_train_df)
    assert y.dtype in ("int32", "int64")


def test_prepare_features_target_encoding(sample_train_df):
    """目标变量 yes/no 应编码为 1/0."""
    _, y = prepare_features(sample_train_df, exclude_cols=["duration"])
    assert set(y.unique()).issubset({0, 1})


def test_build_pipeline_returns_pipeline():
    """构建的 Pipeline 应包含 preprocessor 和 classifier."""
    pipe = build_pipeline(numeric_cols=["age", "salary"], categorical_cols=["job"])
    assert isinstance(pipe, Pipeline)
    assert "preprocessor" in pipe.named_steps
    assert "classifier" in pipe.named_steps


def test_train_and_evaluate(sample_train_df, sample_test_df):
    """训练 + 评估流程应返回有效指标."""
    X_train, y_train = prepare_features(sample_train_df, exclude_cols=["duration"])
    X_test, y_test = prepare_features(sample_test_df, exclude_cols=["duration"])

    num_cols = X_train.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X_train.select_dtypes(include=["object"]).columns.tolist()

    pipe = build_pipeline(num_cols, cat_cols)
    pipe = train_model(pipe, X_train, y_train)

    metrics = evaluate_model(pipe, X_test, y_test)
    assert "accuracy" in metrics
    assert "auc" in metrics
    assert 0.0 <= metrics["auc"] <= 1.0
    assert 0.0 <= metrics["accuracy"] <= 1.0


def test_save_and_load_model(tmp_path, monkeypatch, sample_train_df):
    """模型保存后应能正常加载并推理."""
    import src.model_trainer as mt

    monkeypatch.setattr(mt, "MODEL_DIR", tmp_path)

    X, y = prepare_features(sample_train_df, exclude_cols=["duration"])
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    pipe = build_pipeline(num_cols, cat_cols)
    pipe = train_model(pipe, X, y)

    path = save_model(pipe, model_name="test_model")
    assert path.endswith("test_model.joblib")

    # 加载并预测
    loaded = load_trained_model("test_model")
    pred = loaded.predict(X.head(1))
    assert len(pred) == 1


def test_run_full_training_with_real_data():
    """端到端训练流程应使用真实数据正常完成."""
    from src.model_trainer import run_full_training

    result = run_full_training("train.csv", "test.csv")
    assert "model_path" in result
    assert "metrics" in result
    assert "feature_names" in result
    assert result["metrics"]["auc"] >= 0.0
    assert result["metrics"]["accuracy"] >= 0.0


def test_predictor_with_trained_model():
    """使用真实训练的模型进行预测(集成测试)."""
    from src.predictor import predict_single

    # 构建一个与训练特征匹配的输入
    features = {
        "age": 35,
        "job": "admin.",
        "marital": "married",
        "education": "university.degree",
        "default": "no",
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "month": "may",
        "day_of_week": "mon",
        "campaign": 2,
        "pdays": 999,
        "previous": 0,
        "poutcome": "nonexistent",
        "emp_var_rate": 1.1,
        "cons_price_index": 93.994,
        "cons_conf_index": -36.4,
        "lending_rate3m": 4.67,
        "nr_employed": 4991.6,
    }
    result = predict_single(features)
    assert result["prediction"] in ("会认购", "不会认购")
    assert 0.0 <= result["probability"] <= 1.0
