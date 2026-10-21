# LOL Data and Statistical Design

## Scope and verified data

Study early advantages, match-state patterns, and win prediction in available LCK and LEC games played in 2024 and 2025. The October 20 instructor revision narrows the proposal to three related questions and a primary 15-minute prediction time. The original ten-question bank is historical planning material.

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
- A subsequent source check compared 11 fixed training games with Games of Legends, covering all eight training patches, extreme gold differences, and one zero creep-score difference. All four 15-minute differences, results, dates, patch numbers, and durations agreed. Historical team-name differences were recorded separately. This is a cross-site sample check, not proof of complete coverage or independent upstream measurement; see [source-check report](07_数据来源抽查记录.md).

The audit and cohort creation ran in **R 4.5.2**, using `scripts/01_audit_data.R`. No model was fitted, no hypothesis test was run, and no win-rate or predictive-performance result has been computed.

## Current variables and roles

| Field | Definition and units | Current role |
|---|---|---|
| `game_id` | Unique game identity | Pair the two team rows and retain one game |
| Blue-side `result` | 1 if blue wins, 0 if blue loses | The single primary observed outcome |
| `golddiffat15` | Blue minus red gold | Continuous predictor; scale in thousands |
| `killdiffat15` | Blue minus red kills, derived from paired counts | Continuous/count-difference predictor |
| `xpdiffat15` | Blue minus red experience points | Continuous predictor; scale in thousands |
| `csdiffat15` | Blue minus red creep score, counting minions and monsters killed | Count-difference predictor |
| `patch` | Game-version identifier, preserved as text | Level-2 grouping factor with varying intercept and gold slope |
| `date`, `league` | Actual game date and recorded league | Training, validation, and test partitions; league is not a model coefficient |
| `team_id`, `red_team_id` | Participating team identifiers | Coverage and repeated-team dependence checks |
| 10-minute fields and gold change | Earlier optional snapshot and derived change | Available but outside the primary revised model set |

No final-game total, game result, league-specific fitted test effect, or future team record enters a 15-minute prediction. Duration is a quality check, not a predictor. The earlier team-strength feature, comeback outcome, and side-rate comparison are not required primary models in the revised scope. All three supervised methods estimate the same final blue-side win probability.

## Current model and evaluation plan

See `04_analysis_plan.md` for the authoritative revised plan. Fit and choose models only using Korean 2024 games: 313 games for training, 169 for validation, and their 482-game union for the final refit. Test separately on 555 Korean 2025 games and 306 European 2025 games. The other 294 European 2024 games remain outside model development. Counts and patch-group support were independently rechecked by `scripts/03_check_teacher_revision.R` without fitting outcomes.

The hierarchy has games at level 1 and patches at level 2. The Korean 2024 sample has 12 patches, with 21-70 games per patch. Every 2025 test patch is unseen in source development, so Bayesian predictions integrate new group effects from the learned distribution. Clustering is supporting exploration, not another primary outcome. The three supervised families are pooled logistic regression, Bayesian hierarchical logistic regression, and random forests.

## Sources and snapshot status

- [ChainCC data](https://chaincc.lol/free/data) and [methodology](https://chaincc.lol/about/methodology).
- [Oracle's Elixir downloads](https://oracleselixir.com/tools/downloads): planned checks only; raw files have not yet been obtained.
- Saved URLs, sizes, and hashes: `audit/source_manifest.json`. Live downloads changed after the September snapshot; the local saved files, not current online row counts, support this proposal.
- Earlier 2023 files may be considered separately if needed, but do not enter the primary revised split. Source matching must avoid counting the same match twice.
