"""predictor 模块单元测试."""

import numpy as np
import pandas as pd
import pytest

from src.model_trainer import build_pipeline, prepare_features, save_model, train_model
from src.predictor import predict_batch, predict_single


@pytest.fixture
def trained_model_path(tmp_path, monkeypatch):
    """训练并保存一个临时模型,返回模型目录路径."""
    import src.model_trainer as mt

    monkeypatch.setattr(mt, "MODEL_DIR", tmp_path)

    n = 80
    np.random.seed(42)
    df = pd.DataFrame(
        {
            "age": np.random.randint(20, 65, n),
            "job": np.random.choice(["admin.", "blue-collar", "services"], n),
            "salary": np.random.normal(50000, 15000, n),
            "subscribe": np.random.choice(["no", "yes"], n, p=[0.7, 0.3]),
        }
    )
    X, y = prepare_features(df, exclude_cols=[])
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    pipe = build_pipeline(num_cols, cat_cols)
    pipe = train_model(pipe, X, y)
    save_model(pipe, model_name="test_model")
    return tmp_path


def test_predict_single_returns_expected_keys(trained_model_path, monkeypatch):
    """单条预测结果应包含 prediction 和 probability."""
    import src.predictor as pred_module

    monkeypatch.setattr(
        pred_module,
        "load_trained_model",
        lambda *a, **kw: __import__("joblib").load(
            trained_model_path / "test_model.joblib"
        ),
    )

    features = {"age": 35, "job": "admin.", "salary": 52000.0}
    result = predict_single(features, model_name="test_model")
    assert "prediction" in result
    assert "probability" in result
    assert result["prediction"] in ("会认购", "不会认购")
    assert 0.0 <= result["probability"] <= 1.0


def test_predict_batch_returns_correct_count(trained_model_path, monkeypatch):
    """批量预测应返回与输入等长的结果列表."""
    import src.predictor as pred_module

    monkeypatch.setattr(
        pred_module,
        "load_trained_model",
        lambda *a, **kw: __import__("joblib").load(
            trained_model_path / "test_model.joblib"
        ),
    )

    features_list = [
        {"age": 30, "job": "admin.", "salary": 50000.0},
        {"age": 50, "job": "blue-collar", "salary": 60000.0},
    ]
    results = predict_batch(features_list, model_name="test_model")
    assert len(results) == 2
    for r in results:
        assert r["prediction"] in ("会认购", "不会认购")


def test_predict_single_model_not_found():
    """模型不存在时应抛出错误."""
    with pytest.raises(FileNotFoundError):
        predict_single({"age": 30}, model_name="nonexistent_model")
