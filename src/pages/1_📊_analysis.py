"""数据分析交互页面 — 银行营销数据可视化探索."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_loader import (
    get_categorical_columns,
    get_column_info,
    get_numeric_columns,
    load_data,
)

# ---- 调色板(参考 dataviz skill) ----
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
MAGENTA = "#e87ba4"
SURFACE = "#fcfcfb"
TEXT_SECONDARY = "#52514e"

SUBSCRIBE_COLORS = {"yes": BLUE, "no": ORANGE}


@st.cache_data
def get_data():
    """加载并缓存训练数据."""
    return load_data("train.csv")


def section_overview(df: pd.DataFrame):
    """AC1: 数据集概览."""
    st.header("📋 数据概览")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总行数", f"{len(df):,}")
    col2.metric("总列数", len(df.columns))
    missing_total = int(df.isna().sum().sum())
    col3.metric("缺失值总数", missing_total)
    subscribe_rate = (df["subscribe"] == "yes").mean()
    col4.metric("认购率", f"{subscribe_rate:.1%}")

    st.subheader("列信息")
    info = get_column_info(df)
    info_df = pd.DataFrame(info).T
    info_df.index.name = "列名"
    st.dataframe(info_df, use_container_width=True)


def section_target(df: pd.DataFrame):
    """AC2: 目标变量分布."""
    st.header("🎯 目标变量分布")

    counts = df["subscribe"].value_counts()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=counts.index.map({"yes": "认购", "no": "未认购"}),
            y=counts.values,
            marker_color=[SUBSCRIBE_COLORS.get(k, BLUE) for k in counts.index],
            text=[f"{v:,} ({v / len(df):.1%})" for v in counts.values],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="定期存款认购分布",
        xaxis_title="",
        yaxis_title="客户数量",
        plot_bgcolor=SURFACE,
        showlegend=False,
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


def section_numeric(df: pd.DataFrame):
    """AC3: 数值特征分布 + 分组对比."""
    st.header("📈 数值特征分析")

    numeric_cols = get_numeric_columns(df)
    # 排除 id 列
    numeric_cols = [c for c in numeric_cols if c != "id"]

    if not numeric_cols:
        st.info("无可用数值列。")
        return

    selected = st.selectbox("选择数值特征", numeric_cols, key="num_feat")

    col1, col2 = st.columns(2)
    with col1:
        # 直方图(按 subscribe 分组)
        fig = px.histogram(
            df,
            x=selected,
            color="subscribe",
            color_discrete_map=SUBSCRIBE_COLORS,
            nbins=40,
            marginal="box",
            opacity=0.75,
            barmode="overlay",
            title=f"{selected} 分布(按认购分组)",
        )
        fig.update_layout(plot_bgcolor=SURFACE, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 箱线图
        fig = px.box(
            df,
            x="subscribe",
            y=selected,
            color="subscribe",
            color_discrete_map=SUBSCRIBE_COLORS,
            title=f"{selected} 箱线图(按认购分组)",
        )
        fig.update_layout(plot_bgcolor=SURFACE, height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # 汇总统计
    st.caption(
        f"**{selected}** 认购组中位数: {df[df['subscribe'] == 'yes'][selected].median():.2f}  |  "
        f"未认购组中位数: {df[df['subscribe'] == 'no'][selected].median():.2f}"
    )


def section_categorical(df: pd.DataFrame):
    """AC4: 类别特征分布 + 认购率交叉."""
    st.header("🏷️ 类别特征分析")

    cat_cols = get_categorical_columns(df)
    # 排除目标列
    cat_cols = [c for c in cat_cols if c != "subscribe"]

    if not cat_cols:
        st.info("无可用类别列。")
        return

    selected = st.selectbox("选择类别特征", cat_cols, key="cat_feat")

    # 按 subscribe 分组的频次
    cross = pd.crosstab(df[selected], df["subscribe"])

    fig = go.Figure()
    for sub_val, color in SUBSCRIBE_COLORS.items():
        if sub_val in cross.columns:
            fig.add_trace(
                go.Bar(
                    name="认购" if sub_val == "yes" else "未认购",
                    x=cross.index,
                    y=cross[sub_val],
                    marker_color=color,
                )
            )

    fig.update_layout(
        title=f"{selected} 各类别认购分布",
        xaxis_title=selected,
        yaxis_title="客户数量",
        barmode="stack",
        plot_bgcolor=SURFACE,
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 认购率表
    st.subheader(f"{selected} 各类别认购率")
    rate = (cross["yes"] / cross.sum(axis=1) * 100).sort_values(ascending=False)
    rate_df = pd.DataFrame(
        {
            "类别": rate.index,
            "认购率(%)": rate.round(1).values,
            "样本量": cross.sum(axis=1).values,
        }
    )
    # Reorder rate_df columns to match cross index
    rate_df = rate_df.set_index("类别")
    st.dataframe(rate_df, use_container_width=True)


def section_bivariate(df: pd.DataFrame):
    """AC5: 双变量散点图 + 相关系数."""
    st.header("🔗 双变量关系")

    numeric_cols = [c for c in get_numeric_columns(df) if c != "id"]

    if len(numeric_cols) < 2:
        st.info("数值列不足2列,跳过双变量分析。")
        return

    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("X 轴", numeric_cols, index=0, key="x_col")
    with col2:
        y_col = st.selectbox(
            "Y 轴", numeric_cols, index=min(1, len(numeric_cols) - 1), key="y_col"
        )

    if x_col == y_col:
        st.warning("请选择不同的两列。")
        return

    corr = df[[x_col, y_col]].corr().iloc[0, 1]
    st.metric("Pearson 相关系数", f"{corr:.4f}")

    # 采样以避免散点图过密
    sample = df.sample(min(3000, len(df)), random_state=42)
    fig = px.scatter(
        sample,
        x=x_col,
        y=y_col,
        color="subscribe",
        color_discrete_map=SUBSCRIBE_COLORS,
        opacity=0.6,
        title=f"{x_col} vs {y_col}",
    )
    fig.update_traces(marker={"size": 6})
    fig.update_layout(plot_bgcolor=SURFACE, height=500)
    st.plotly_chart(fig, use_container_width=True)


def section_quality(df: pd.DataFrame):
    """AC6: 数据质量标注."""
    st.header("⚠️ 数据质量")

    info = get_column_info(df)
    missing_cols = {k: v for k, v in info.items() if v["missing_count"] > 0}

    if missing_cols:
        st.warning(f"发现 {len(missing_cols)} 列含缺失值:")
        for col, detail in missing_cols.items():
            st.markdown(
                f"- `{col}`: {detail['missing_count']} 条缺失 ({detail['missing_pct']}%)"
            )
    else:
        st.success("未发现缺失值。")

    # 检查未知值
    for col in get_categorical_columns(df):
        if "unknown" in df[col].values or "nonexistent" in df[col].values:
            unknown_count = (df[col].isin(["unknown", "nonexistent"])).sum()
            st.info(
                f"`{col}` 含 `unknown`/`nonexistent` 值: {unknown_count} 条 ({unknown_count / len(df):.1%})"
            )


# ---- 主页面 ----
st.set_page_config(page_title="数据分析", page_icon="📊", layout="wide")
st.title("📊 银行营销数据分析")

df = get_data()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📋 数据概览", "🎯 目标分布", "📈 数值特征", "🏷️ 类别特征", "🔗 双变量 & 质量"]
)

with tab1:
    section_overview(df)
with tab2:
    section_target(df)
with tab3:
    section_numeric(df)
with tab4:
    section_categorical(df)
with tab5:
    section_bivariate(df)
    st.divider()
    section_quality(df)
