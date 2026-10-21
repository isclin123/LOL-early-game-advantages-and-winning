# Early Game Advantages and Winning in League of Legends

A course capstone on professional League of Legends. Each game is summarised by four
measures at the 15-minute mark, and the project asks what those early advantages are
worth and whether a model built on them travels.

1. **How are 15-minute advantages related to winning?**
2. **Does the gold–win relationship vary across game patches?**
3. **Do models trained in Korea predict games in another league and year?**

The outcome is whether the blue side wins the game: 1 or 0, with the probability
estimated from the state at 15 minutes. The predictors are the blue-minus-red gaps in
gold, kills, experience and creep score, each summed over the five players on a side.

## Status

Everything lives in one reproducible file, [`analysis/LoL_Project.Rmd`](analysis/LoL_Project.Rmd).

| Section | What it covers | State |
| --- | --- | --- |
| 1–4 | Sources, preprocessing, variable dictionary, frozen splits | Complete |
| 5 | Exploratory analysis of the 313 training games | Complete |
| 6 | Saved artefacts and reproducibility outputs | Complete |
| 7 | Logistic regression baseline, diagnostics, validation scoring | Complete |
| 8 | Bayesian hierarchical model, random forest, clustering | Not started |
| 9 | Frozen specification and the two final tests | Not started |
| 10 | Discussion and conclusions | Not started |

**Neither 2025 test set has been scored.** `analysis/artifacts/baseline_checks.json`
records `test_partitions_scored: false` and `test_partitions_read: false`, and they stay
that way until every modelling choice is frozen in section 9.

## Data

A saved export from [ChainCC](https://chaincc.lol/free/data). The three `.csv.gz` files in
`data/raw/` are frozen; their SHA-256 hashes are checked on every render against
`audit/source_manifest.json`.

One row is one game, with the two team rows paired into a single blue-side record — the
export ships each game twice as exact mirrors, so counting both would double the sample
for no information.

| | Games |
| --- | ---: |
| Candidates in the export | 3,159 |
| Dropped: one league with an unusable early gold field | −1,522 |
| **Retained** | **1,637** |

Eleven training games were checked field by field against Games of Legends; all 44
early-statistic comparisons agreed. Details and the limits of that check are in
`07_数据来源抽查记录.md`.

## Study design

Chronological, never random: a random split would put games from the same week, even the
same series, on both sides.

| Partition | League and period | Games | Patches |
| --- | --- | ---: | ---: |
| Training | Korea, Jan–Jun 2024 | 313 | 8 |
| Validation | Korea, Jul–Sep 2024 | 169 | 4 |
| Refit (union of the two above) | Korea, all of 2024 | 482 | 12 |
| Test — time transfer | Korea, 2025 | 555 | 13 |
| Test — region transfer | Europe, 2025 | 306 | 12 |
| Deliberately unused | Europe, 2024 | 294 | 8 |

Europe 2024 is held out of development on purpose: training on it would mean the model had
already seen European teams, and Europe 2025 would stop being a clean test of a new region.
Every game of a series stays inside one partition, which is verified in code.

## What the baseline found

| Model | Games | Log loss | Brier | AUC |
| --- | --- | ---: | ---: | ---: |
| Four predictors | Training, 313 | 0.5039 | 0.168 | 0.828 |
| Four predictors | Validation, 169 | **0.5162** | 0.173 | 0.818 |
| Training win rate only | Validation, 169 | 0.6927 | 0.250 | 0.500 |

Lower log loss is better. The reference predicts the training win rate for every game and
scores essentially log 2 — the score for having no information.

Three diagnostics shape how the rest of the project is written:

- **No separation.** All four measures overlap between wins and losses. The largest gold
  lead in a losing game is 3,915; the smallest in a winning one is −3,299.
- **Coefficients are not interpretable.** Each predictor is 77–88% explained by the other
  three (largest variance inflation factor 8.0). Dropping the 15 most influential games
  flips the sign of the kill coefficient, while no single game is influential (largest
  Cook's distance 0.04). Predicted probabilities are reported instead.
- **Team strength is missing.** Three of ten teams have a mean residual more than two
  standard errors from zero. Team indicators are not added, because they could not
  transfer to the 2025 European test.

## Layout

```
analysis/        LoL_Project.Rmd and its rendered output, figures and saved artefacts
data/raw/        the three frozen ChainCC exports
data/derived/    the eligible-games cohort
scripts/         R and Python audit scripts, plus the proposal builder
audit/           data-readiness, split, toolchain and external source checks
output/          the one-page proposal as PDF, Word and Markdown
archive/, tmp/   earlier drafts kept for history
```

Planning documents, numbered `01`–`07`, cover the data and methods, the analysis plan, the
point-by-point response to instructor feedback, and the execution plan. `06`, `07` and
`README_使用说明.md` are written in Chinese.

## Reproducing

R 4.5.2 with rtools45. The analysis needs `knitr`, `ggplot2`, `jsonlite` and `digest`;
section 8 will also need `brms` 2.23.0 and `ranger` 0.18.0, both verified to compile and
sample here by `scripts/09_check_toolchain.R`.

```bash
Rscript --vanilla -e 'rmarkdown::render("analysis/LoL_Project.Rmd", output_format = "all")'
```

Rendering from a terminal needs pandoc on the path. If only RStudio's copy is installed,
point `RSTUDIO_PANDOC` at `<RStudio>/resources/app/bin/quarto/bin/tools` first; knitting
from inside RStudio needs no such step. The file locates itself whether it is knitted or
run chunk by chunk, so a personal `.Rprofile` that calls `setwd()` will not break it.

Individual checks can be re-run on their own:

```bash
Rscript --vanilla scripts/04_audit_data_readiness.R
```

## Limits

These are observational games, so every relationship is an association rather than the
effect of handing a team gold. Teams recur across weeks, so the games are not independent.
The sample is a saved snapshot of one export, not every official game played. Any shortfall
on a test set mixes version change, roster turnover and shifts in playstyle, and this design
does not attribute it to any one of them.

Saved HTML copies of the third-party pages used in the source check are excluded by
`.gitignore`. The manifests beside them record every URL with its SHA-256, and the
field-by-field comparison results are kept.
