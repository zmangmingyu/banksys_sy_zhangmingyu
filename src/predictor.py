"""预测推理模块.

负责加载已训练模型并对单条/批量输入进行预测.
"""

import pandas as pd

from src.model_trainer import load_trained_model


def predict_single(features: dict, model_name: str = "model_pipeline") -> dict:
    """对单条输入进行预测.

    Args:
        features: 特征名 → 特征值的字典.
        model_name: 模型文件名(不含扩展名).

    Returns:
        dict: {prediction: "会认购"|"不会认购", probability: float}.
    """
    model = load_trained_model(model_name)
    df = pd.DataFrame([features])
    proba = model.predict_proba(df)[:, 1][0]
    prediction = "会认购" if proba >= 0.5 else "不会认购"
    return {
        "prediction": prediction,
        "probability": round(float(proba), 4),
    }


def predict_batch(
    features_list: list[dict], model_name: str = "model_pipeline"
) -> list[dict]:
    """对批量输入进行预测.

    Args:
        features_list: 特征字典列表.
        model_name: 模型文件名.

    Returns:
        list[dict]: 预测结果列表.
    """
    model = load_trained_model(model_name)
    df = pd.DataFrame(features_list)
    probas = model.predict_proba(df)[:, 1]
    results = []
    for proba in probas:
        prediction = "会认购" if proba >= 0.5 else "不会认购"
        results.append(
            {
                "prediction": prediction,
                "probability": round(float(proba), 4),
            }
        )
    return results
