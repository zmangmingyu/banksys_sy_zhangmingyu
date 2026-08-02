"""Streamlit 应用入口基础测试."""

import subprocess
import sys
from pathlib import Path


def test_app_module_importable():
    """app.py 应能被 Python 正常导入,不触发运行时错误."""
    _ = Path(__file__).resolve().parent.parent / "src" / "app.py"
    result = subprocess.run(
        [sys.executable, "-c", "import src.app"],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parent.parent),
        check=False,
    )
    # Streamlit 导入可能输出警告,但不应该有 Traceback
    assert "Traceback" not in result.stderr, f"Import failed: {result.stderr}"


def test_data_loader_importable():
    """data_loader 模块应可导入."""
    from src.data_loader import get_column_info, load_data

    assert callable(load_data)
    assert callable(get_column_info)


def test_model_trainer_importable():
    """model_trainer 模块应可导入."""
    from src.model_trainer import build_pipeline, evaluate_model, train_model

    assert callable(build_pipeline)
    assert callable(train_model)
    assert callable(evaluate_model)


def test_predictor_importable():
    """predictor 模块应可导入."""
    from src.predictor import predict_batch, predict_single

    assert callable(predict_single)
    assert callable(predict_batch)
