# 🏦 银行营销数据分析与认购预测系统

基于银行营销数据的交互式数据分析与在线预测 Web 应用。

## 功能

| 功能 | 说明 |
|---|---|
| 📊 **数据分析** | 多维度交互式可视化：概览、数值/类别特征分布、双变量关系、数据质量检查 |
| 🔮 **在线预测** | 点选表单输入客户特征,实时返回认购意向预测 + 概率 |

## 技术栈

```
Python 3.11 · Streamlit · scikit-learn · Plotly · pytest · ruff · Docker
GitHub Actions (CI/CD)
```

## 目录结构

```
├── src/
│   ├── app.py                # Streamlit 多页入口
│   ├── pages/
│   │   ├── 1_📊_analysis.py  # 数据分析页
│   │   └── 2_🔮_prediction.py# 在线预测页
│   ├── data_loader.py        # 数据加载与统计
│   ├── model_trainer.py      # Pipeline 训练与评估
│   ├── predictor.py          # 模型推理
│   └── utils.py              # 工具函数
├── tests/                    # 单元测试(覆盖率 ≥ 80%)
├── data/                     # UCI Bank Marketing 数据集
├── .github/workflows/
│   ├── ci.yml                # CI: ruff + pytest + docker build
│   └── cd.yml                # CD: SSH → 构建 → 部署 → 健康检查
├── Dockerfile                # Python 3.11-slim,构建时训练模型
└── standards/                # 项目规范与进度记录
```

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt -r requirements-dev.txt

# 2. 启动应用
streamlit run src/app.py --server.port 8888

# 3. 浏览器访问
http://localhost:8888
```

## 测试

```bash
# 格式检查
ruff format --check .

# 静态检查
ruff check .

# 单元测试 + 覆盖率
pytest --cov=src --cov-fail-under=80
```

## Docker

```bash
# 构建(含模型训练)
docker build -t banksys .

# 运行
docker run -d --name banksys --restart unless-stopped -p 8888:8888 banksys

# 健康检查
curl http://localhost:8888/_stcore/health
```

## 部署

合并 `main` 分支后 GitHub Actions 自动:

1. **CI**: ruff → pytest → docker build
2. **CD**: rsync 代码 → Docker 构建 → 端口 8888 → 健康检查

## 模型

- 算法: Logistic Regression (Pipeline: StandardScaler + OneHotEncoder)
- 验证 AUC: ~0.81
- 特征: 19 列(不含 `duration`,因预测时不可获知)
- 数据: UCI Bank Marketing (~30,000 条)

## 环境变量 (CD Secrets)

| Secret | 说明 |
|---|---|
| `SSH_PRIVATE_KEY` | 部署到服务器的 SSH 私钥 |
| `SSH_HOST` | 服务器 IP/域名 |
| `SSH_USER` | 服务器登录用户 |
