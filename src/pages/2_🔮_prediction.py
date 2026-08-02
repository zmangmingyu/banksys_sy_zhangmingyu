"""在线预测交互页面 — 客户认购意向预测."""

import streamlit as st

from src.predictor import predict_single

st.set_page_config(page_title="在线预测", page_icon="🔮", layout="wide")
st.title("🔮 客户认购意向预测")

st.markdown("填写以下客户特征,点击**预测**按钮获得认购意向判断。")

# ---- 类别字段选项(从训练集提取) ----
CATEGORICAL_FIELDS = {
    "job": [
        "admin.",
        "blue-collar",
        "entrepreneur",
        "housemaid",
        "management",
        "retired",
        "self-employed",
        "services",
        "student",
        "technician",
        "unemployed",
        "unknown",
    ],
    "marital": ["married", "single", "divorced", "unknown"],
    "education": [
        "university.degree",
        "high.school",
        "professional.course",
        "basic.9y",
        "basic.6y",
        "basic.4y",
        "illiterate",
        "unknown",
    ],
    "default": ["no", "yes", "unknown"],
    "housing": ["yes", "no", "unknown"],
    "loan": ["no", "yes", "unknown"],
    "contact": ["cellular", "telephone"],
    "month": ["may", "jun", "jul", "aug", "oct", "nov", "dec", "mar", "apr", "sep"],
    "day_of_week": ["mon", "tue", "wed", "thu", "fri"],
    "poutcome": ["nonexistent", "failure", "success"],
}

# ---- 默认值(取众数或中位数) ----
DEFAULTS = {
    "job": "admin.",
    "marital": "married",
    "education": "university.degree",
    "default": "no",
    "housing": "yes",
    "loan": "no",
    "contact": "cellular",
    "month": "may",
    "day_of_week": "thu",
    "poutcome": "nonexistent",
    "age": 38,
    "campaign": 1,
    "pdays": 999,
    "previous": 0,
    "emp_var_rate": 1.1,
    "cons_price_index": 93.99,
    "cons_conf_index": -36.4,
    "lending_rate3m": 4.67,
    "nr_employed": 4991.6,
}

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👤 个人特征")
        age = st.number_input(
            "年龄 (age)", min_value=16, max_value=101, value=DEFAULTS["age"], step=1
        )
        job = st.selectbox(
            "职业 (job)",
            CATEGORICAL_FIELDS["job"],
            index=CATEGORICAL_FIELDS["job"].index(DEFAULTS["job"]),
        )
        marital = st.selectbox(
            "婚姻 (marital)",
            CATEGORICAL_FIELDS["marital"],
            index=CATEGORICAL_FIELDS["marital"].index(DEFAULTS["marital"]),
        )
        education = st.selectbox(
            "教育 (education)",
            CATEGORICAL_FIELDS["education"],
            index=CATEGORICAL_FIELDS["education"].index(DEFAULTS["education"]),
        )

    with col2:
        st.subheader("💰 财务特征")
        default = st.selectbox(
            "违约 (default)",
            CATEGORICAL_FIELDS["default"],
            index=CATEGORICAL_FIELDS["default"].index(DEFAULTS["default"]),
        )
        housing = st.selectbox(
            "房贷 (housing)",
            CATEGORICAL_FIELDS["housing"],
            index=CATEGORICAL_FIELDS["housing"].index(DEFAULTS["housing"]),
        )
        loan = st.selectbox(
            "贷款 (loan)",
            CATEGORICAL_FIELDS["loan"],
            index=CATEGORICAL_FIELDS["loan"].index(DEFAULTS["loan"]),
        )

    with col3:
        st.subheader("📞 联络特征")
        contact = st.selectbox(
            "联络方式 (contact)",
            CATEGORICAL_FIELDS["contact"],
            index=CATEGORICAL_FIELDS["contact"].index(DEFAULTS["contact"]),
        )
        month = st.selectbox(
            "联络月份 (month)",
            CATEGORICAL_FIELDS["month"],
            index=CATEGORICAL_FIELDS["month"].index(DEFAULTS["month"]),
        )
        day_of_week = st.selectbox(
            "联络星期 (day_of_week)",
            CATEGORICAL_FIELDS["day_of_week"],
            index=CATEGORICAL_FIELDS["day_of_week"].index(DEFAULTS["day_of_week"]),
        )

    st.divider()
    st.subheader("📊 活动 & 经济背景")

    col4, col5, col6 = st.columns(3)
    with col4:
        campaign = st.number_input(
            "联络次数 (campaign)",
            min_value=0,
            max_value=60,
            value=DEFAULTS["campaign"],
            step=1,
        )
        pdays = st.number_input(
            "距上次联络天数 (pdays)",
            min_value=0,
            max_value=1050,
            value=DEFAULTS["pdays"],
            step=1,
        )
        previous = st.number_input(
            "历史联络次数 (previous)",
            min_value=0,
            max_value=10,
            value=DEFAULTS["previous"],
            step=1,
        )

    with col5:
        poutcome = st.selectbox(
            "上次活动结果 (poutcome)",
            CATEGORICAL_FIELDS["poutcome"],
            index=CATEGORICAL_FIELDS["poutcome"].index(DEFAULTS["poutcome"]),
        )
        emp_var_rate = st.number_input(
            "就业变化率 (emp_var_rate)",
            min_value=-5.0,
            max_value=5.0,
            value=DEFAULTS["emp_var_rate"],
            step=0.1,
            format="%.1f",
        )
        cons_price_index = st.number_input(
            "消费价格指数 (cons_price_index)",
            min_value=85.0,
            max_value=105.0,
            value=DEFAULTS["cons_price_index"],
            step=0.01,
            format="%.2f",
        )

    with col6:
        cons_conf_index = st.number_input(
            "消费信心指数 (cons_conf_index)",
            min_value=-60.0,
            max_value=-20.0,
            value=DEFAULTS["cons_conf_index"],
            step=0.1,
            format="%.1f",
        )
        lending_rate3m = st.number_input(
            "3个月利率 (lending_rate3m)",
            min_value=0.0,
            max_value=10.0,
            value=DEFAULTS["lending_rate3m"],
            step=0.01,
            format="%.2f",
        )
        nr_employed = st.number_input(
            "就业人数 (nr_employed)",
            min_value=4500.0,
            max_value=5500.0,
            value=DEFAULTS["nr_employed"],
            step=0.1,
            format="%.1f",
        )

    submitted = st.form_submit_button(
        "🔮 预测", type="primary", use_container_width=True
    )

# ---- 预测结果 ----
if submitted:
    features = {
        "age": age,
        "job": job,
        "marital": marital,
        "education": education,
        "default": default,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "month": month,
        "day_of_week": day_of_week,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "poutcome": poutcome,
        "emp_var_rate": emp_var_rate,
        "cons_price_index": cons_price_index,
        "cons_conf_index": cons_conf_index,
        "lending_rate3m": lending_rate3m,
        "nr_employed": nr_employed,
    }

    try:
        result = predict_single(features)
        proba_pct = result["probability"] * 100

        if result["prediction"] == "会认购":
            st.success(f"### ✅ 预测: {result['prediction']}")
            st.metric("认购概率", f"{proba_pct:.1f}%")
        else:
            st.warning(f"### ❌ 预测: {result['prediction']}")
            st.metric("认购概率", f"{proba_pct:.1f}%")

        # 进度条可视化
        st.progress(result["probability"], text=f"认购倾向: {proba_pct:.1f}%")
    except FileNotFoundError:
        st.error("模型文件未找到。请先在服务器上运行模型训练。")
    except ValueError as e:
        st.error(f"预测失败(输入错误): {e}")
