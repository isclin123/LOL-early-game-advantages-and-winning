# Analysis Plan and Difficulty Levels

This is a planned master's-level statistical study, not a report of fitted models. The main question is how early advantages relate to winning and how well those relationships describe future professional League of Legends games. The project uses one checked cohort, ten related questions, and R throughout. The difficulty comes from asking different statistical questions, checking assumptions, and evaluating uncertainty and transfer over time.

## Shared data and outcome

The main sample remains the 1,637 available LCK/LEC games dated 2024-2025 in the audited ChainCC files: 776 games in 2024 and 861 in 2025. Structural checks and field definitions are in `01_data_and_methods.md`. Match counts are not independent effective sample sizes; teams play repeatedly and games may belong to the same series.

An additional R feasibility check found finite values and nonzero variation in all eight early numerical features, 562 games meeting Q2's deficit threshold, and 26 patches with 9 to 115 games each. It also confirmed three chronological training/validation splits containing both leagues: 393/140, 533/134, and 667/109 games. These checks do not use win rates or fitted models; they establish structural feasibility, not statistical power or measurement accuracy. The record is `audit/revised_design_feasibility.md`.

Each observation is one game, oriented to blue side. Let `y = 1` if blue side wins. At minute `t`, define `g_t`, `k_t`, `xp_t`, and `cs_t` as blue-minus-red gold, kill, experience, and creep-score differences. Context includes league and a pregame team-strength difference. Q2 reorients the final outcome to the trailing side only after identifying that side from the 15-minute gold gap; it still counts one observation per game.

Gold differences are expressed in thousands, XP in thousands, and CS in tens for readable regression coefficients. Standardization for clustering and the Bayesian prior scale uses the relevant development sample. Final-game totals and duration are not early predictors; duration only establishes that a snapshot could exist. Genuine zero differences must be distinguished from zero-filled missing snapshots. Snapshot completeness, numerical ranges, and source definitions receive an additional check before modeling.

## Level 1 Descriptive inference for Q1 and Q2

Q1 reports blue-side win proportions by league and their difference, with year-specific summaries. An adjusted logistic model with league and prior team strength is a sensitivity check, not proof of a side or league effect.

Q2 defines a comeback as winning after trailing by at least 2,000 gold at 15 minutes. Report eligible games and comeback events together. Predeclare deficit bands [2000, 4000) and [4000, infinity); do not choose cutoffs after seeing which gives the largest contrast. Overall and subgroup proportions use calendar-week block bootstrap confidence intervals, with 1,000 resamples as the starting setting.

If a subgroup has very few or no comeback events, show counts and state that the rate is poorly determined. A zero-width bootstrap interval with no observed events is not reliable evidence of a zero population rate. An exact binomial interval may be shown only as a sensitivity calculation that assumes independent games; it does not solve dependence. Historical supplementation may help a comparable overall comeback estimate but cannot add observations to an already completed individual patch.

## Level 2 Regression for Q3 to Q5

Use logistic regression for the binary outcome. The main interpretable 15-minute model is:

```r
glm(y ~ splines::ns(g15, df = 3) + k15 + xp15 + cs15 + league + elo_diff,
    family = binomial(), data = development)
```

This is a planned formula, not fitted code or a result. Q3 first compares a linear gold term with the three-degree-of-freedom natural spline, keeping league and strength controls identical. Nonlinearity here concerns the log-odds relationship; a sigmoid probability curve is already possible with linear logistic regression. Compare validation log loss and plot uncertainty over observed, supported gold ranges rather than extrapolating into rare extreme leads.

Q4 compares the gold-and-context model with models that add kills, XP, and CS separately and jointly. Conditional coefficients answer different questions from their raw associations. Examine correlation and coefficient uncertainty, and assess the three indicators jointly. Report unstable individual estimates transparently rather than assigning causal importance to them.

Q5 uses the initial gold gap and `delta_gold = g15 - g10`. A model may contain `ns(g10, df = 3) + delta_gold + league + elo_diff`. It must not also include a linear `g15` term together with the corresponding initial and change terms because those terms are linearly dependent. The change formulation does not add information beyond both original snapshots and does not identify psychological momentum.

Model checks include convergence and separation, influential games, calibration, and uncertainty under week-block refits. Address failures transparently instead of deleting inconvenient observations. The inferential focus is estimated relationships and uncertainty; the ten questions are an exploratory set, not ten independent confirmatory tests.

## Level 3 Clustering and transfer for Q6 and Q7

Q6 fits k-means to four 15-minute differences in the 2024 sample. Center and scale each feature using 2024 values only. Keep the fixed blue-side orientation and exclude win/loss, team identity, league, and patch from the clustering features. Clusters describe match states, not persistent team styles or strategies.

Consider K = 2, 3, 4, and 5, with 50 random starts per K and a recorded seed. Compare average silhouette width, profiles, and stability. As a practical size check, avoid interpreting clusters smaller than the larger of 30 games and 5 percent of the development sample. These are project choices, not universal reliability thresholds. A PCA plot can show the four-dimensional data in two dimensions; PCA is for visualization, not an additional input transformation in the main clustering model.

Assess stability by resampling entire 2024 calendar weeks 200 times. Refit the scaler and k-means for each resample, assign the original development games to that fit, and compare memberships with the original solution using the adjusted Rand index. Repeat across candidate K values. Select a solution using separation, stability, and size without looking at outcomes. If separation is weak across all choices, report that evidence favors a continuous advantage gradient rather than claim discovery of natural categories. Correlated gold, XP, and CS may all emphasize that gradient; examine this limitation explicitly.

For Q7, freeze K, 2024 means/scales, and centers. Apply the same transformation to 2025 games and assign each to its nearest center without refitting. Compare profiles, group sizes, average distances to centers, and silhouettes, then summarize group win rates with uncertainty. A partition always assigns points, so assignment itself does not demonstrate transfer. If Q6 gives weak groups, Q7 documents this weakness rather than treating those groups as validated categories. Group win differences are descriptive and may reflect the same gold information used to construct the groups.

## Level 4 Bayesian hierarchical inference for Q8

Q8 is a retrospective analysis of variation across the 26 observed patch codes. Use standardized gold and pregame strength, a league fixed effect, and patch-specific intercepts and gold slopes. A starting model is:

```r
brms::brm(
  y ~ g15_z + league + elo_z + (1 + g15_z || patch),
  family = brms::bernoulli(link = "logit"), data = analysis_data,
  prior = c(
    brms::prior(normal(0, 1.5), class = Intercept),
    brms::prior(normal(0, 1), class = b),
    brms::prior(exponential(1), class = sd)
  )
)
```

This is a starting specification. Independent patch intercept and slope deviations avoid adding an extra correlation parameter to a limited sample. Partial pooling expresses an exchangeability assumption after the included controls; patches are not literally independent randomized interventions. Gold effects may be nonlinear, so compare the linear hierarchical model with a sensitivity model that adds a shared quadratic gold term under a regularizing prior. Prior predictive checks must verify that the implied probabilities and curvature are reasonable over the observed range.

Compare posterior patch curves with a complete-pooling model using the same common terms. Report posterior medians, 95 percent credible intervals, and the posterior distribution of between-patch variation. Smaller groups may be more strongly influenced by the common distribution, but neither narrow intervals nor nonzero variation are guaranteed. To assess sensitivity, change the coefficient prior scale and group standard-deviation prior while keeping data and estimands fixed.

Start with four chains, inspect trace plots, R-hat (target below 1.01), bulk and tail effective sample sizes, Monte Carlo standard errors, and divergent transitions. Increase computation or revise an ill-conditioned model when diagnostics require it. Use posterior predictive checks by gold band, league, and patch. Sensitivity to a calendar-week random intercept examines some short-term dependence; repeated teams and time-confounded patches remain limitations even if sampling diagnostics pass.

The model may use both years for retrospective inference only after predictive recipes are frozen and final predictive evaluation is complete. Do not use its fitted 2025 patch effects as inputs to the 2025 prediction test. It estimates observed patch differences, not causal effects of balance changes. New-patch prediction would need integration over the population distribution of patch effects and is outside the main comparison.

## Level 5 Statistical learning for Q9 and Q10

Use two model families: logistic regression with a modest spline for gold and probability random forests. Clustering provides unsupervised learning, while random forests provide a flexible supervised comparison with logistic regression. The project includes all three requested areas of regression, clustering, and Bayesian inference, plus these supervised comparisons.

All models receive the same raw information: the four statistics at the stated minute, league, and prior team strength. The logistic comparator uses the Q3/Q4 spline form. The forest uses the original numeric features and league and can learn nonlinearities and interactions directly. A 2024 training-prevalence forecast and an early-statistics-free league-plus-strength logistic model are simple performance references.

For random forests, use 500 trees, candidate mtry values {2, 3, 6}, minimum node sizes {10, 25, 50}, and depth limits {3, 6}. Fix other settings and use probability predictions, not just hard class votes. These starting grids keep the workload proportionate to 776 development games. The exact grid may be revised during 2024 development, but it must be frozen before the 2025 test is examined. No additional algorithm is required merely to increase the count of methods.

Q9 compares the two 15-minute models. Q10 adds their 10-minute counterparts with the same fold structure and tuning budget. Reuse the 15-minute fits; this is a two-model by two-time-point comparison, not a separate project for each question. Compare within-family timing differences and between-family differences at 15 minutes. Later information is allowed to improve prediction but reduces the time remaining before the final result.

## Common temporal validation and uncertainty

1. Use 2024 only for model development and cluster discovery. Within 2024, order the weeks with observed games. Use the first half of those weeks for initial training, followed by three contiguous validation blocks covering the remaining weeks; expand the training window after each block. Keep every game's two source rows paired and all games in a week within the same block.
2. Refit scaling, spline knots, any missing-value treatment, and forest tuning within each training fold. Check that fold models are estimable and have support for both leagues. Use held-out log loss to choose hyperparameters; do not use random row-level cross-validation or out-of-bag errors as the main time-transfer estimate.
3. Refit each frozen recipe on all 2024 games and evaluate once on the same eligible 2025 games. The main cohort has complete audited snapshot fields; any later source correction must be documented before freezing. Model-based imputation cannot rescue unavailable early snapshots that were filled with zeros.
4. Pregame Elo starts new teams at 1500, uses K = 20 and a 400-point logistic scale, and carries over into 2025. Update only from games whose results were available before the target game. Batch identical timestamps, confirm timestamp meanings, and use a conservative earlier-day cutoff if exact availability is uncertain. Earlier completed 2025 results may update this predeclared historical feature for later 2025 games; model coefficients and hyperparameters remain frozen. Report cold starts and roster changes; omit each team's first five observed games as a sensitivity analysis.
5. The primary predictive measure is log loss. Also report Brier score, AUC, and calibration plots with fixed probability bands and group counts. Clip probabilities to [1e-6, 1 - 1e-6] for finite log loss and report this convention. Calibration assesses whether probabilities agree with observed frequencies; accuracy alone is insufficient. Do not recalibrate on the test outcomes.
6. For model and timing contrasts, use identical resampled 2025 calendar-week blocks for paired bootstrap intervals with 1,000 resamples. Keep fitted models fixed during this test-sample bootstrap; the intervals describe evaluation-sample uncertainty, not all uncertainty from model development. A two-week block sensitivity can probe stronger dependence. Repeated teams across blocks remain a limitation.
7. Keep 2025 outcome summaries, Q7 win-rate analyses, and full-cohort Q1-Q5/Q8 association analyses from influencing the frozen predictive recipes. Once the predictive comparison is complete, report broader retrospective analyses as exploratory. Do not select only positive findings or claim that whichever model won the test was independently validated on an additional dataset.

## Supplementary data and scope control

Seek Oracle's Elixir records to check match dates, coverage, and missing snapshot fields. ChainCC already lists it as a historical source, so matching records are not additional independent games. Resolve duplicates by match identity, teams, time, and source identifiers; uncertain matches should not be silently joined. Raw Oracle files have not yet been obtained, and this remains a planned check.

Checked 2023 LCK/LEC games could support separate historical robustness analyses or initialize earlier team strength. Keep the main 2024-development/2025-test comparison intact and label any expansion. Adding 2023 observations does not increase the sample of a particular 2024/2025 patch. Player-level data are unnecessary for these ten questions; introducing player roles or draft composition would require a separate change to the research scope and variable checks.

The target is feasible modeling and honest uncertainty, not a promise that every method finds a strong effect. Only source feasibility and structural checks have been run. No regression, clustering, Bayesian model, or predictive model has yet been fitted.

## R tools and primary references

- Data and figures: `dplyr` and `ggplot2`; base R suffices for core preparation.
- Regression: [`stats::glm`](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/glm.html) and [`splines::ns`](https://stat.ethz.ch/R-manual/R-devel/library/splines/html/ns.html).
- Clustering: [`stats::kmeans`](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/kmeans.html), [`cluster::silhouette`](https://stat.ethz.ch/R-manual/R-devel/library/cluster/html/silhouette.html), and [`mclust::adjustedRandIndex`](https://mclust-org.github.io/mclust/reference/adjustedRandIndex.html) for a label-invariant stability comparison.
- Bayesian inference: [`brms`](https://paulbuerkner.com/brms/) and [Stan convergence diagnostics](https://mc-stan.org/learn-stan/diagnostics-warnings.html); successful model sampling requires a working Stan backend and compiler, to be checked when analysis begins.
- Supervised learning: [`ranger`](https://imbs-hl.github.io/ranger/).
- Evaluation: `pROC` for AUC, direct probability scores for log loss and Brier score, and base R for paired block resampling.

These references support implementation choices. Full course lectures and the instructor's complete rubric were not present; the plan does not claim that every advanced method has already been taught in this course.
