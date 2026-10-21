# LOL Data and Statistical Design

## Scope and verified data

Study early advantages, match-state patterns, and win prediction in available LCK and LEC games played in 2024 and 2025. The ten questions are all retained in the one-page proposal. The main analysis uses information recorded at 10 and 15 minutes, not final-game statistics as early predictors.

Primary download source: [ChainCC Open LoL Esports Dataset](https://chaincc.lol/free/data). Its [methodology](https://chaincc.lol/about/methodology) identifies Oracle's Elixir as a source of historical professional drafts and scoreboards. ChainCC is a third-party data provider, not Riot's official dataset. The files are licensed CC BY 4.0 according to the download page. Frozen URLs and SHA-256 hashes are in `audit/source_manifest.json`.

Files labelled 2024, 2025, and 2026 were downloaded to identify records by actual match date rather than the file-year label. Together they contain 59,184 team-game rows and 29,592 unique game IDs. The selected 2024–2025 LCK/LEC sample contains **1,637 unique games**, with one blue-side analysis row per game. The two team rows were paired by game ID before creating differences.

| Actual year | LCK games | LEC games | Total |
|---|---:|---:|---:|
| 2024 | 482 | 294 | 776 |
| 2025 | 555 | 306 | 861 |
| Total | 1,037 | 600 | 1,637 |

This is the coverage present in the checked snapshot, not a claim that every official game in these leagues is included. The selected dates range from January 13, 2024 to September 28, 2025. There are 26 patch codes, some with small samples.

### Data quality decisions

- The original candidate cohort included LPL as well, with 3,159 games across the three leagues. All 1,522 LPL games in this cohort have nonpositive early total-gold fields, so they cannot support this early-game project. LPL is excluded; its zero-filled early differences must not be treated as tied games.
- Required fields in the retained LCK/LEC cohort contain no blank or NA values. Both teams have positive total gold at 10 and 15 minutes, all games last longer than 15 minutes, and outcomes are complementary.
- No repeated game-side keys were found across the three source files. Recorded gold differences agree with differences in the two teams' total gold; signed differences are opposite across sides. These are structural consistency checks, not a complete independent verification against match recordings.
- Some deaths exceed the opposing team's kills, which can occur with executions. Such records were not removed merely because deaths and opposing kills differ. No retained game has opposing kills exceeding recorded deaths at 15 minutes.
- Read `patch` as text: codes such as `14.10` must not be converted to numeric `14.1`. Use actual dates to select years, and preserve raw files unchanged.
- Future analysis should check the meaning and completeness of the early snapshots against source documentation and a small match sample, especially zero-valued XP or CS differences. A genuine zero difference is possible and is not automatically missing.

The audit and cohort creation ran in **R 4.5.2**, using `scripts/01_audit_data.R`. No model was fitted, no hypothesis test was run, and no win-rate or predictive-performance result has been computed.

## Variables

| Variable | Meaning and units | Use |
|---|---|---|
| `game_id` | Unique game identifier | Pair the two teams; keep one analysis row per game |
| `date`, `league`, `patch` | Actual date, LCK/LEC, and version code | Cohort definition, temporal evaluation, and context |
| `side` | Blue or Red in the raw file | Keep Blue as the fixed modelling orientation; Q1 compares its win rate with 0.5 |
| `result` | TRUE if that side wins | Binary response `y = 1` for a blue-side win |
| `team_id`, `red_team_id` | IDs of both teams | Create historical strength features from earlier games only |
| `golddiffat10`, `golddiffat15` | Blue gold minus red gold at the stated minute | Main explanatory variables; divide by 1,000 for regression units |
| `killdiffat10`, `killdiffat15` | Blue kills minus red kills at the stated minute | Derived by joining the two sides' kill counts |
| `xpdiffat10`, `xpdiffat15` | Blue experience minus red experience | Scale by 1,000 XP for regression |
| `csdiffat10`, `csdiffat15` | Blue creep score minus red creep score | Scale by 10 CS for regression |
| `goldgain10to15` | Gold difference at 15 minus gold difference at 10 | Change in the advantage; not total gold earned |
| `trailing_win` | Whether the team behind at 15 minutes later wins | For Q2, derive once per game using the sign of the gold difference |
| `deficit15` | Absolute gold difference at 15 minutes | Q2 uses a predeclared threshold of at least 2,000 gold |
| Pregame Elo difference | Historical blue-team rating minus red-team rating | An imperfect adjustment for relative team strength, calculated without the current result |

Final kills, final gold, full-game objective counts, and game length are **not** predictors in a 10- or 15-minute forecast. Duration is used only to confirm that the target snapshot exists. No first-blood or first-dragon event is assumed to occur before 15 minutes without a timestamp. Champion names are available but do not need to be added to this deliberately focused first proposal.

## Updated analysis design

The question numbering and methods have been revised together. Q1-Q2 estimate side and comeback proportions; Q3-Q5 use logistic regression for nonlinear and conditional relationships; Q6-Q7 use k-means and assess transfer to a later year; Q8 uses Bayesian hierarchical logistic regression across patches; Q9-Q10 compare logistic regression, elastic net, and random forests at two prediction times.

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
