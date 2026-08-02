"""Streamlit 应用入口 — 多页银行营销数据分析与预测系统."""

import streamlit as st

st.set_page_config(
    page_title="银行营销数据分析与认购预测",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏦 银行营销数据分析与认购预测系统")

st.markdown("""
欢迎使用银行营销数据分析与认购预测系统。

- **数据分析**: 在侧边栏选择 *数据分析* 页面,探索客户特征与认购行为。
- **在线预测**: 在侧边栏选择 *预测系统* 页面,输入客户信息获取认购预测。
""")

st.info("请使用左侧导航栏切换功能页面。")
