# PROGRESS · 项目进度 〔本项目活记忆 · AI 维护〕

> **作用**:记录当前进度、下一步 TODO、关键决策(ADR)、踩坑记录(GOTCHAS)。
> **更新时机**:每完成一个模块/步骤、每遇到并解决一个坑、每做一次关键决策时更新。
> **排序规则**:时间倒序,最新的在最上面。

---

## 1. 当前状态

- **六步流程位置**:第 0 步(准备阶段) — 已完成上下文文档与需求编写,等待人工确认后进入第①步(建仓)。
- **最后更新**:2026-08-02

---

## 2. 下一步 TODO

> 优先级从高到低;[] 标记进度。

### 第一批:工程基础(US-1)

- [ ] **TODO-1** 建仓 + 初始化项目骨架
  - 创建 GitHub 仓库
  - 写入 `.gitignore`、`requirements.txt`、`requirements-dev.txt`、`Dockerfile`、`.dockerignore`
  - 搭建 `src/`、`tests/` 目录结构
  - 写入 `.github/workflows/ci.yml`(ruff + pytest + docker build)
  - 写入 `.github/workflows/cd.yml`(SSH 部署 + 健康检查)
  - 确认分支:`feature/1-project-init`

- [ ] **TODO-2** 实现 Streamlit 应用入口 + 健康检查
  - `src/app.py` 多页应用入口(含 `/healthz` 健康检查端点)
  - 各页占位骨架(`pages/1_analysis.py`、`pages/2_prediction.py`)
  - 写入 `tests/test_app.py`

- [ ] **TODO-3** 本地 CI 自检 → PR → 合并(US-1 验收)
  - ruff format + ruff check + pytest 全绿
  - 发起 PR,等待 CI 通过
  - 人工合并 → CD 部署 → 验证端口 8888

### 第二批:数据分析页(US-2)

- [ ] **TODO-4** 实现数据加载模块 + 测试
  - `src/data_loader.py`:加载 CSV、基础统计、缺失值检测
  - `tests/test_data_loader.py`

- [ ] **TODO-5** 实现分析页交互式可视化
  - `pages/1_analysis.py`:概览、分布、交叉分析、散点/相关性
  - 更新 PROGRESS 汇报进度

### 第三批:模型训练(US-3)

- [ ] **TODO-6** 实现模型训练模块 + 测试
  - `src/model_trainer.py`:预处理管道 + 分类模型训练 + 评估 + 保存
  - `tests/test_model_trainer.py`
  - 验证 AUC ≥ 0.75

### 第四批:在线预测(US-4)

- [ ] **TODO-7** 实现预测推理模块 + 测试
  - `src/predictor.py`:加载模型 + 单条/批量推理
  - `tests/test_predictor.py`

- [ ] **TODO-8** 实现预测交互页面
  - `pages/2_prediction.py`:表单 + 预测展示
  - 端到端验证

### 第五批:收尾(US-5)

- [ ] **TODO-9** 编写 README.md
- [ ] **TODO-10** 最终 CI/CD 全链路验证

---

## 3. ADR(架构决策记录)

_暂无。将在实现过程中逐条追加。_

<!-- 模板:
### ADR-1 <决策标题> · 2026-XX-XX
- **背景**:<为什么需要决策>
- **决策**:<选择了什么>
- **替代方案**:<考虑过哪些其他方案>
- **后果**:<带来的影响>
-->

---

## 4. GOTCHAS(踩坑记录)

_暂无。将在开发/部署过程中逐条追加。_

<!-- 模板:
### GOTCHA-1 <问题简述> · 2026-XX-XX
- **现象**:<具体表现>
- **根因**:<为什么发生>
- **修复**:<怎么解决的>
- **预防**:<如何避免再次发生>
-->
