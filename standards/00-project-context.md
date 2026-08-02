# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的"身份档案"。AI 接管项目时先读这里,了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。

---

## 1. 项目是什么

- **项目名称**:`banksys_sy_zhangmingyu`
- **一句话目标**:基于银行营销数据,提供交互式数据分析与在线预测系统,帮助业务人员洞察客户并预测认购意向。
- **使用者/受益者**:银行业务人员 / 营销团队,通过可视化分析理解客户特征,通过预测模型筛选高意向客户。
- **核心功能**:
  - **交互式数据分析页面**:对银行营销数据进行多维度可视探索(分布、相关性、交叉分析等)。
  - **在线预测系统**:基于历史数据离线训练分类模型,提供 Web 表单(点选输入客户特征),实时返回是否会认购定期存款。
- **输入/数据**:
  - 来源:`data/train.csv`(训练集,22,500 条)、`data/test.csv`(测试集,7,500 条)。
  - 数据类型:银行营销活动记录,含客户人口统计、财务指标、联络信息、经济背景共 21 列(含目标列 `subscribe`)。
  - 敏感程度:公开教学数据集(UCI Bank Marketing 衍生),无个人隐私。
  - 是否进 Git:数据为公开 UCI 教学数据,进 Git;模型产物不进 Git;代码与配置进 Git。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 项目指定版本,生态成熟(数据科学 + Web 均支持) |
| Web/应用框架 | Streamlit | 纯 Python 构建数据应用与交互式仪表板,适合快速交付数据分析与预测界面 |
| 机器学习 | scikit-learn | 经典银行营销分类任务,生态完整,模型可解释,部署轻量 |
| 测试 | pytest | 项目指定,Python 生态标准测试框架 |
| 格式/静态检查 | ruff | 项目指定,统一格式 + lint,速度快 |
| 打包/运行 | Docker | 项目指定,保证本地/CI/CD/服务器环境一致 |
| CI/CD | GitHub Actions | 项目指定,通用、可视化、适合教学与团队协作 |

## 3. 目录地图

```text
banksys_sy_zhangmingyu/
├── standards/                     # AI 项目记忆与通用规范
│   ├── README.md
│   ├── 00-project-context.md      # 本文件
│   ├── 01-requirements.md         # 活 PRD
│   ├── PROGRESS.md                # 进度记录
│   ├── 02-coding-standards.md
│   ├── 03-testing-standards.md
│   ├── 04-git-workflow.md
│   ├── 05-cicd-standards.md
│   ├── 06-ai-collab-protocol.md
│   └── templates/
├── data/                          # 数据集(不进 Git)
│   ├── train.csv
│   └── test.csv
├── src/                           # 应用源码
│   ├── __init__.py
│   ├── app.py                     # Streamlit 应用入口(多页)
│   ├── pages/                     # Streamlit 多页子模块
│   │   ├── __init__.py
│   │   ├── 1_analysis.py          # 页1:数据分析交互
│   │   └── 2_prediction.py        # 页2:在线预测
│   ├── data_loader.py             # 数据加载与预处理
│   ├── model_trainer.py           # 模型离线训练逻辑
│   ├── predictor.py               # 预测服务(加载模型+推理)
│   └── utils.py                   # 公共工具
├── models/                        # 训练产出模型文件(不进 Git)
├── tests/                         # 测试
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_model_trainer.py
│   ├── test_predictor.py
│   └── test_app.py
├── requirements.txt               # 生产运行依赖
├── requirements-dev.txt           # 本地/CI 检查依赖
├── Dockerfile                     # 容器构建
├── .dockerignore
├── .gitignore
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
└── README.md
```

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | 核心代码 ≥ 80% |
| 构建 | `docker build` 成功 |
| 业务/模型指标 | 模型 AUC ≥ 0.75;预测接口 200 响应 |

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**,只进 GitHub Secrets / 环境变量。
- 大文件、数据集、模型产物不进 Git(通过 `.gitignore` 排除 `data/`、`models/`)。
- `main` 分支受保护,日常开发必须走 feature 分支 + PR。
- CI 红灯不合并。

## 6. 部署/CI 占位符取值

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `banksys` | 应用名/镜像名/容器名 |
| `<DEPLOY_DIR>` | `/opt/banksys` | 服务器部署目录 |
| `<PORT>` | `8888` | 服务端口 |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `/_stcore/health` | 健康检查地址(Streamlit 内置) |
| `<SSH_USER>` | `<deploy 用户,由学生配置>` | 部署用户 |
| `<SSH_HOST>` | `<服务器 IP 或域名,由学生配置>` | 服务器地址 |
