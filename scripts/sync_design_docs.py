"""Keep the data guide and Chinese navigation aligned with the revised proposal."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if 'teacher_feedback_2026-10-20' in (ROOT / 'proposal_content.json').read_text(encoding='utf-8'):
    raise SystemExit('Historical sync disabled for the teacher revision; current guides are maintained directly.')
path = ROOT / '01_data_and_methods.md'
text = path.read_text(encoding='utf-8')
marker = '## Analysis plan shared by the ten questions'
if marker not in text:
    marker = '## Updated analysis design'
text = text.split(marker)[0]
text = text.replace('For Q7, derive once per game', 'For Q2, derive once per game')
text = text.replace('Q7 uses a predeclared threshold', 'Q2 uses a predeclared threshold')
text = text.replace(
    'Study how early advantages relate to winning in available LCK and LEC games played in 2024 and 2025.',
    'Study early advantages, match-state patterns, and win prediction in available LCK and LEC games played in 2024 and 2025.'
)
text += '''## Updated analysis design

The question numbering and methods have been revised together. Q1-Q2 estimate side and comeback proportions; Q3-Q5 use logistic regression for nonlinear and conditional relationships; Q6-Q7 use k-means and assess transfer to a later year; Q8 uses Bayesian hierarchical logistic regression across patches; Q9-Q10 compare logistic regression and random forests at two prediction times.

The full current specifications, priors, cluster checks, and shared validation rules are in [Analysis Plan and Difficulty Levels](04_analysis_plan.md). The per-question variables, methods, expectations, keywords, and four sentences are in [Ten Research Questions](02_ten_research_questions.md). These replace the earlier regression-only question numbering and analysis plan.

The main predictive split remains 2024 for development and 2025 for testing. Preprocessing and model selection stay within chronological 2024 folds. Cluster selection excludes outcomes. Full-cohort Bayesian and descriptive analyses follow the frozen predictive evaluation and cannot be used to retune the tested models. Repeated teams, small groups, and source coverage remain limitations.

## Planned source checks and supplementation

Seek Oracle's Elixir records to verify dates, coverage, and missing snapshot fields, while matching games and removing duplicates. This is a planned source check, not a second independently verified sample: raw Oracle files have not yet been obtained. ChainCC already lists Oracle's Elixir as a historical source.

Checked 2023 LCK/LEC records may support supplementary historical analyses when definitions are comparable. They do not enlarge any particular 2024/2025 patch. Keep the main 2024-2025 comparison intact and distinguish expanded analyses. No player-level dataset is required for the revised ten questions.

## Sources

1. [ChainCC data page](https://chaincc.lol/free/data).
2. [ChainCC source methodology](https://chaincc.lol/about/methodology).
3. [2024 team file](https://chaincc.lol/data/chaincc-teams-2024.csv.gz), [2025 team file](https://chaincc.lol/data/chaincc-teams-2025.csv.gz), and [2026 team file](https://chaincc.lol/data/chaincc-teams-2026.csv.gz). File labels do not define the selected date range.
4. [Oracle's Elixir downloads](https://oracleselixir.com/tools/downloads), a planned cross-check source whose files are not yet obtained.
5. Primary method documentation is linked in `04_analysis_plan.md`.
'''
path.write_text(text, encoding='utf-8')
(ROOT / 'README_使用说明.md').write_text('''# LOL 统计学硕士课程项目

主题：**Early Game Advantages and Winning in League of Legends**。研究前期优势、比赛模式与最终胜负，把回归、聚类、贝叶斯分析和机器学习组织在同一条主线上。

提交稿仍是**一页英文、明确列出 10 个问题、使用 R、附数据源链接、不写 Semester Plan**。非专业英语尽量简单，统计术语保持准确。完整研究设计单独保存，不把四十句话挤进一页。

## 文件

- `output/LoL_Project_Proposal.pdf`：一页英文提交稿。
- `output/LoL_Project_Proposal.docx`：可编辑 Word 稿。
- `output/LoL_Project_Proposal.md`：同内容纯文本稿。
- `02_ten_research_questions.md`：10 题的完整设计，每题包含数据、变量、方法、R 工具、预期结果、限制、关键词和四句话。
- `04_analysis_plan.md`：难度层次、模型设定、先验、聚类稳定性、调参和跨年份验证。
- `01_data_and_methods.md`：数据质量、来源、变量定义及补充数据计划。
- `audit/data_audit.md`：已经完成的 R 数据核验记录。

## 五个难度层次和十个问题

| 层次 | 问题 | 方法与学习重点 |
|---|---|---|
| 基础统计 | Q1 蓝方胜率在 LCK 与 LEC 是否不同；Q2 落后至少 2,000 经济后的翻盘率 | 比例估计、分组比较、区间与样本依赖 |
| 回归分析 | Q3 经济与胜负的关系是否需要非线性项；Q4 击杀、经验和补刀能否提供额外信息；Q5 控制初始经济差后，扩大优势是否与胜负有关 | Logistic regression、样条、共线性、条件关系 |
| 多元分析 | Q6 前期比赛能否分成稳定的模式；Q7 2024 年发现的模式在 2025 年是否仍适用及其胜率差异 | K-means、标准化、silhouette、重抽样稳定性和跨年份迁移 |
| 贝叶斯分析 | Q8 不同版本下经济优势与胜负的关系如何变化 | 分层 logistic regression、partial pooling、先验敏感性、后验预测检验 |
| 机器学习预测 | Q9 随机森林能否超过逻辑回归；Q10 各模型从 10 分钟到 15 分钟能提高多少预测表现 | 非线性模型、时间顺序调参、校准与配对比较 |

Q9 和 Q10 共用两个模型家族，每个模型做两个时间点，共四种主要模型配置；Q10 直接复用 Q9 的 15 分钟模型。Q6 与 Q7 共用同一套聚类。这样每种方法都有实际研究任务，工作量也能控制。机器学习不一定优于逻辑回归，聚类不一定有明显边界，贝叶斯分层模型也不保证每个版本都有精确答案。

## 数据与可行性

实际下载的 ChainCC 文件标签为 2024、2025、2026，再按真实日期筛选。当前主样本为 **1,637 场 LCK/LEC 比赛：2024 年 776 场，2025 年 861 场**。这只是快照内可用比赛，不声称完整覆盖所有官方赛事。

候选数据中 LPL 的 1,522 场缺少可用的 10／15 分钟经济字段，并有零填充，不能当作真实经济持平，因此未纳入。当前仅完成结构核验，正式建模前还需核对早期字段定义和抽样记录。

Oracle's Elixir 用于计划中的来源核对，尚未取得其原始文件。它可能与 ChainCC 记录同一批比赛，不能直接相加当作更多样本。经过检查的 2023 年 LCK/LEC 比赛可用于补充历史分析，主比较仍保留 2024 建模、2025 检验；其他年份不能增加某个特定版本的实际样本量。

## 让研究达到硕士水平的关键

- 一场比赛保留一行，处理两队配对及重复战队带来的依赖。
- 聚类只用前期数值，不用胜负来选组数；还要检查稳定性及下一年是否适用。
- 贝叶斯分析明确先验、层次结构和可信区间，并检查采样诊断及模型是否能重现数据特征。
- 所有预测模型统一数据和验证规则，只在 2024 年内按时间调参；2025 年用于冻结方案后的评价。
- 预测不只看准确率，还看 log loss、Brier score、AUC、calibration 和改善幅度的不确定性。
- 全年贝叶斯与描述性分析可以在预测评价完成后开展，但不能反过来调整已测试的预测模型。

目前没有拟合回归、聚类、贝叶斯或机器学习模型，也没有计算这些问题的答案。Proposal 中的预期都是待检验的假设。课程讲义和完整 rubric 不在当前文件夹，因此这里是按统计学硕士水平设计的方法方案，不代表老师确认过的课程方法清单。

## 复现与历史版本

`scripts/01_audit_data.R` 复核现有数据，统计分析计划使用 R。`scripts/download_data.py` 仅下载公共数据；`scripts/build_proposal.py` 和 `scripts/build_question_designs.py` 仅生成文档。文档生成工具不是统计分析工具。

`tmp/before_methods_redesign/` 保存本次改版前的稿件。上一级目录中的 Dota 2 文件属于旧选题，不是当前提交版本。
''', encoding='utf-8')
print('Updated data guide and Chinese navigation.')
