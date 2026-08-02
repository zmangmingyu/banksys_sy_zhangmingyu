# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里,不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 用户 / 老师 / 产品 / 客户 | 写成用户故事 |
| 缺陷 Bug | 测试 / 线上日志 / 用户反馈 | 写复现步骤和期望结果 |
| 技术债 Tech Debt | 开发 / Review / CI/CD 故障 | 写影响和修复目标 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI 和 Review |
| 合并 | Done | PR 合并 main,自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**:分支名带 Issue 号,PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 初始化项目工程化与 CI/CD 管线 · 状态: Backlog

作为 **项目开发者**,
我想要 项目具备基础工程结构、测试、CI 与 CD 管线,
以便 后续每次开发都能自动检查并自动部署。

验收标准:
- AC1: Given 空仓库,When 完成初始化,Then 项目包含 `src/`、`tests/`、`requirements.txt`、`requirements-dev.txt`、`Dockerfile`、`.github/workflows/ci.yml`、`.github/workflows/cd.yml`。
- AC2: Given 提交 PR,When CI 触发,Then 依次通过 ruff format、ruff check、pytest(覆盖率 ≥ 80%)、docker build。
- AC3: Given 合并 main,When CD 触发,Then 自动 SSH 部署到服务器、构建镜像并运行容器,健康检查 `/healthz` 返回 200。
- AC4: Given 项目根目录,When 启动 Streamlit,Then 在 `8888` 端口提供 Web 服务。
- AC5: Given `.gitignore`,When 检查仓库,Then `data/`、`models/`、`__pycache__/`、`.pytest_cache/` 均被排除。

技术备注:
- 本地不强制 Docker,但 CI 必须包含 `docker build` 检查。
- 生产依赖与开发依赖分离(`requirements.txt` vs `requirements-dev.txt`)。
- 健康检查端点 `/healthz` 由 Streamlit 挂载或独立 ASGI 端点提供。

---

### US-2 银行营销数据探索分析页 · 状态: Backlog

作为 **银行业务分析师**,
我想要 在 Web 页面上对营销数据进行交互式可视化分析,
以便 快速理解客户分布、识别影响认购的关键因素、发现营销机会。

验收标准:
- AC1: Given 应用已启动,When 用户打开分析页面,Then 页面展示数据集概览(总行数、列名、各列类型、缺失值统计)。
- AC2: Given 目标变量 `subscribe`,When 查看分布,Then 以适当的图表展示 yes/no 占比。
- AC3: Given 数值型特征(age、duration、campaign 等),When 用户选择某列,Then 展示该列的直方图/箱线图及其与目标变量的分组对比。
- AC4: Given 类别型特征(job、marital、education 等),When 用户选择某列,Then 展示各类别的频次柱状图及与认购率的交叉表。
- AC5: Given 两列数值特征,When 用户选择某两列,Then 展示散点图(按 subscribe 着色)及相关系数。
- AC6: Given 数据存在缺失值或异常值,When 页面加载,Then 以醒目方式标注数据质量问题位置与数量。

技术备注:
- 使用 Streamlit 原生图表组件或 Plotly 渲染,确保交互性(tooltip、缩放)。
- 数据加载使用缓存(`@st.cache_data`),避免每次交互重读 CSV。
- 经济背景列(`emp_var_rate`、`cons_price_index` 等)可能具有强多重共线性,分析页可提示但不必自动处理。

---

### US-3 离线模型训练与评估模块 · 状态: Backlog

作为 **数据科学家**,
我想要 使用历史营销数据离线训练一个认购预测分类模型并保存,
以便 后续在线预测系统加载该模型提供实时推理。

验收标准:
- AC1: Given `data/train.csv`,When 运行训练脚本,Then 完成数据预处理(编码、标准化、处理缺失值)并输出预处理器的配置(可序列化)。
- AC2: Given 预处理后的训练数据,When 训练模型,Then 至少训练一个分类模型(如 Logistic Regression 或 Random Forest),并输出 AUC ≥ 0.75。
- AC3: Given 训练完成的模型,When 在 `data/test.csv` 上评估,Then 输出准确率、精确率、召回率、F1、AUC,四项指标均写入日志。
- AC4: Given 训练完成,When 保存模型,Then 预处理管道与模型一并序列化保存到 `models/` 目录,可通过单行代码加载并推理。
- AC5: Given 模块代码,When 运行 `pytest tests/test_model_trainer.py`,Then 所有训练相关测试通过。

技术备注:
- 必须使用 Pipeline 将预处理与模型打包,避免在线推理时预处理不一致。
- `duration` 列为通话时长,真实场景中预测时此列未知(在通话前),模型训练时应评估"有 duration"与"无 duration"两种特征集的性能差异;默认使用**无 duration**特征集,但训练日志中报告两种结果。
- 类别编码推荐 OneHotEncoder 或 OrdinalEncoder(对有序类别),数值标准化推荐 StandardScaler。

---

### US-4 在线认购预测系统 · 状态: Backlog

作为 **银行业务人员**,
我想要 通过一个点选表单输入客户特征,点击预测按钮后立即获知该客户是否会认购,
以便 在营销活动中快速筛选高意向客户,提升转化效率。

验收标准:
- AC1: Given 已加载预训练模型,When 用户打开预测页面,Then 以表单形式展示所有必需输入字段(age、job、marital、education、default、housing、loan、contact、month、day_of_week、campaign、pdays、previous、poutcome、emp_var_rate、cons_price_index、cons_conf_index、lending_rate3m、nr_employed)。
- AC2: Given 表单字段,When 用户交互,Then 所有类别型字段使用下拉选择框(selectbox),数值型字段使用数值输入框(number_input)或滑块(slider),并预设合理默认值。
- AC3: Given 表单已完整填写,When 用户点击"预测"按钮,Then 调用预训练模型推理,在页面显示预测结果("会认购" / "不会认购")及对应置信度/概率。
- AC4: Given 非法或缺失输入,When 用户点击预测,Then 页面给出清晰的字段级错误提示,不崩溃。
- AC5: Given 预测完成,When 用户修改输入并再次点击,Then 结果实时更新,无需刷新页面。
- AC6: Given 预测页面,When 运行 `pytest tests/test_predictor.py`,Then 模型加载、单条推理、批量推理、边界输入测试均通过。

技术备注:
- 表单字段顺序与 `train.csv` 列顺序一致,确保用户体验连贯。
- 默认值取各列的众数(类别)或中位数(数值),降低用户输入成本。
- 禁止将 `duration` 作为预测输入(真实场景无法提前获知通话时长);若模型训练时使用 duration,需在预测页明确提示并给出替代方案。
- 使用 Streamlit 的 `st.form` 确保用户主动提交后才推理,避免每次按键触发推理。

---

### US-5 项目文档与 README · 状态: Backlog

作为 **新加入的开发者或运维人员**,
我想要 一份清晰的 README 文档,
以便 能在 5 分钟内了解项目目标、本地启动步骤、测试方法、部署方式。

验收标准:
- AC1: Given README,When 阅读,Then 包含项目简介、技术栈、目录结构说明。
- AC2: Given README,When 开发者按步骤操作,Then 能在本地完成环境配置 → 启动应用 → 访问 `http://localhost:8888`。
- AC3: Given README,When 开发者运行,Then 明确列出本地测试命令(`ruff format --check .`、`ruff check .`、`pytest`)。
- AC4: Given README,When 运维人员阅读,Then 说明 Docker 构建与运行方式、所需环境变量、健康检查地址。

---

## 5. 非功能需求

- **安全**:密钥只进 Secrets,不进 Git;预测服务不暴露训练数据原始记录。
- **可维护**:一需求一小 PR,避免大爆炸式提交;Streamlit 页面与业务逻辑分离(`pages/` 只做 UI,`src/` 做逻辑)。
- **可测试**:核心逻辑必须有单元测试;数据加载、预处理、模型训练、预测推理各模块独立可测。
- **可部署**:部署后必须有健康检查 `/healthz`;Docker 镜像 ≤ 500MB(不含数据)。
- **可复现**:固定随机种子(`random_state=42`);`requirements.txt` 锁定依赖版本。
- **响应时间**:预测接口单次推理 ≤ 2 秒;数据分析页首次加载 ≤ 5 秒(含 CSV 读取)。
