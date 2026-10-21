# LOL Data and Statistical Design

## Scope and verified data

Study how early advantages relate to winning in available LCK and LEC games played in 2024 and 2025. The ten questions are all retained in the one-page proposal. The main analysis uses information recorded at 10 and 15 minutes, not final-game statistics as early predictors.

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
| `trailing_win` | Whether the team behind at 15 minutes later wins | For Q7, derive once per game using the sign of the gold difference |
| `deficit15` | Absolute gold difference at 15 minutes | Q7 uses a predeclared threshold of at least 2,000 gold |
| Pregame Elo difference | Historical blue-team rating minus red-team rating | An imperfect adjustment for relative team strength, calculated without the current result |

Final kills, final gold, full-game objective counts, and game length are **not** predictors in a 10- or 15-minute forecast. Duration is used only to confirm that the target snapshot exists. No first-blood or first-dragon event is assumed to occur before 15 minutes without a timestamp. Champion names are available but do not need to be added to this deliberately focused first proposal.

## Analysis plan shared by the ten questions

**Descriptive questions.** Q1 summarizes blue-side winning frequency. Q7 summarizes the comeback rate among games with an absolute 15-minute gold difference of at least 2,000. Each game contributes one outcome, including when orienting it to the trailing side. Report group sizes alongside all proportions; an unadjusted side comparison is not a causal estimate of side advantage.

**Gold and additional indicators.** Use logistic regression for the binary outcome. For Q2, model the gold difference at 15 minutes with a natural cubic spline with 3 degrees of freedom. For Q3–Q5, add kill, experience, or CS difference individually to the same gold-and-context model; this avoids interpreting highly correlated early statistics as independent causal effects. For Q6, use gold difference at 10 and its change to 15 as predictors; do not include those two terms and gold difference at 15 together because of their exact linear relationship.

**Context and strength.** Use league and historical team-strength difference as shared controls. Elo starts every newly observed team at 1500, uses K = 20 and the usual 400-point logistic scale, and updates once per game after its recorded result. Construct ratings in actual date/time order from available LCK/LEC games; games sharing a timestamp use ratings before that time block, then update together. The current outcome is never available to its own predictors. Carry ratings from 2024 into 2025 without a season reset, and report cold starts and roster changes as limitations. A sensitivity analysis can omit each team's first five observed games.

**League and patch comparisons.** Q8 adds a league-by-gold interaction and compares winning-probability curves over the gold range supported in both leagues. Q9 uses descriptive curves and a logistic model with patch intercepts and linear patch-by-gold interactions for patches with at least 50 games. Smaller patch samples receive descriptive counts only; report insufficient support rather than merging unrelated patches after examining outcomes. Patch comparisons are exploratory and confounded with time, teams, and changes in competition format; they do not identify the causal effect of an update.

**Prediction at 10 versus 15 minutes.** Q10 compares the same predeclared model forms at each time: league, pregame Elo difference, a 3-degree-of-freedom spline of gold difference, and linear kill, XP, and CS differences. Use the same eligible games for both forecasts. Use 2024 for model development and 2025 for final prediction evaluation. Learn spline knots, centering/scaling, and any other preprocessing from 2024 only. If tuning becomes necessary, use rolling chronological validation within 2024, not random row-level folds. Freeze the recipe before examining 2025 outcome associations or predictive scores. After the final predictive evaluation, all-year descriptive and patch analyses may be reported as exploratory without changing the frozen models.

**Evaluation and uncertainty.** Primary predictive comparison: the difference in 2025 log loss between the two models. Also report Brier score, AUC, accuracy at a fixed 0.5 threshold, and calibration plots. Clip probabilities to [1e-6, 1 - 1e-6] only for finite log loss. Use a paired bootstrap of whole calendar-week blocks, keeping games together and using identical resampled weeks for both models, with 1,000 replicates. For association summaries, use the same block principle to avoid treating every game as fully independent. Repeated teams across weeks remain a limitation; block intervals do not eliminate all dependence. Treat the ten questions as a planned exploratory set and emphasize effect sizes and uncertainty rather than selecting only significant results.

**Implementation scope.** Use base R (`stats`, `splines`) for regression, `dplyr` for data preparation, `ggplot2` for figures, and `pROC` for AUC. No deep learning, live prediction service, scraping system, or deployment is required. All ten questions are part of the project; the one-page proposal gives the short version and the question bank records each design.

## Sources

1. [ChainCC data page](https://chaincc.lol/free/data).
2. [ChainCC data-source and methodology description](https://chaincc.lol/about/methodology).
3. [2024 team file](https://chaincc.lol/data/chaincc-teams-2024.csv.gz), [2025 team file](https://chaincc.lol/data/chaincc-teams-2025.csv.gz), [2026 team file](https://chaincc.lol/data/chaincc-teams-2026.csv.gz). File labels do not define the selected date range.
4. [R natural spline documentation](https://stat.ethz.ch/R-manual/R-devel/library/splines/html/ns.html).
