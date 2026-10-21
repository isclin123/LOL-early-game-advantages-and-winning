# Revised Analysis Plan

Revision: October 20, 2026, following the instructor's eleven comments. This plan supersedes the earlier ten-question analysis plan. The earlier question bank is retained as planning history, not ten required analyses. No models have been fitted and no outcome relationships have been estimated.

## Main question and three related parts

The main question is whether early-game advantages provide useful estimates of the chance of winning, including outside the competition used to build a model.

1. **Early indicators:** How are 15-minute gold, kill, experience, and creep-score differences related to winning? Use logistic regression for conditional associations and probability curves. Random forests assess nonlinear predictive relationships. Clustering is a supporting description, not a separate required research objective.
2. **Patch variation:** Does the gold-win relationship vary across game patches? Use Bayesian hierarchical logistic regression with explicit game and patch levels.
3. **Transfer:** Do models built using Korean games predict later Korean games and games in another league? Compare the same frozen models on two 2025 test sets.

The former side-rate, comeback, gold-change, cluster-transfer, and 10-versus-15-minute questions are no longer separate core deliverables. The main prediction time is 15 minutes. A later 10-minute sensitivity analysis is optional and cannot change the predeclared primary test. No unfamiliar penalized regression method is included.

## Data and clearly defined outcomes

Use the saved ChainCC snapshot, not a silently refreshed download. The saved cohort contains 1,637 paired games dated 2024-2025. League of Legends Champions Korea is recorded as `LCK`. League of Legends EMEA Championship is recorded as `LEC`; EMEA means Europe, the Middle East and Africa. The short submission avoids these abbreviations and uses descriptive league names. Names and regions can be checked against [Riot Games](https://competitiveops.riotgames.com/en-US/league-of-legends).

The response for every supervised model is `y = 1` when the blue-side team wins the game and `y = 0` when it loses. The prediction is the probability of that final outcome using information available at 15 minutes. A game, rather than a series or a player, is the unit of analysis. Pair the blue and red source records and retain one observation per game. The sample is conditional on games with valid 15-minute measurements; it does not represent games missing that snapshot.

The four common predictors are signed blue-minus-red differences in gold, kills, experience, and creep score, the count of minions and monsters killed. Units and source fields are in `01_data_and_methods.md`. Patch is the recorded game-version code. Date and league define the partitions. Team identifiers support dependence and coverage checks; they are not predictive fixed effects or clustering features. The revised primary models omit the earlier derived team-strength feature to keep inputs directly observed and comparable across leagues. Unmeasured team strength therefore remains an explicit limitation.

There is no additional response called cluster membership or patch effect: clusters are descriptive summaries, patch parameters describe heterogeneity, and the final observed response remains binary game victory. Report probabilities, probability-score differences, and uncertainty without confusing them with additional outcomes.

## Training validation and two untouched tests

The partition was checked in R using `scripts/03_check_teacher_revision.R`. The corresponding record is `audit/teacher_revision_feasibility.md`; proposed game identifiers are stored in `audit/proposed_teacher_split_ids.rds`.

| Role | League and dates | Games | Use |
|---|---|---:|---|
| Training | Korean league, January-June 2024 | 313 | Initial preprocessing, model fitting, and diagnostics |
| Validation | Korean league, July-September 2024 | 169 | Choose model settings and assess later source-league performance |
| Final source refit | All Korean games in 2024 | 482 | Refit selected recipes before touching either test outcome set |
| Temporal test | Korean league, 2025 | 555 | Evaluate transfer to a new year within the source league |
| External test | European regional league, 2025 | 306 | Evaluate transfer to a different league and year |
| Outside the primary analysis | European regional league, 2024 | 294 | Retained in the saved pool; not used for fitting, tuning, or the primary tests |

The final refit row is the union of training and validation, not another independent sample. The five disjoint partitions excluding that refit row sum to 1,637. Actual observed source dates end on September 8, 2024; both 2025 tests end on September 28. The calendar descriptions do not imply complete coverage of every official game.

Learn centering, scaling, and any model-based preprocessing on the 313 training games when evaluating validation performance. Freeze choices using only those training and validation data, then relearn the same preprocessing recipe on the 482-game refit set. Apply that saved transformation to both tests. Test outcomes must never select model form, hyperparameters, calibration adjustments, cluster count, or priors. Source validation is modest in size; keep choices few and predeclare comparison rules.

League is not a predictor in these fits: only one league appears in development, so there is no estimated European-league coefficient. Do not fit on the external league and call its later performance an untouched transfer test. Both 2025 sets are scored separately, and the cross-league performance gap is descriptive rather than a causal regional effect.

## Common model set

**Logistic regression.** Start with `y ~ gold15 + kills15 + experience15 + creep15`, using interpretable scales or training-only standardization. Examine correlations among predictors, separation, residual patterns against each predictor, leverage, and influential games. Compare a predeclared spline gold term with the linear form only on source validation if the functional-form check suggests a problem. Report conditional probability contrasts and uncertainty rather than interpreting coefficients as effects of giving a team extra gold.

**Random forest.** Fit a probability forest to the same four predictors using `ranger` in R. Use a modest grid, for example 500 trees, candidate numbers of split variables 2 or 4, and minimum split-node sizes 10 or 25, with a fixed seed. Choose settings by validation log loss. Examine the gap between training and validation scores. Use validation plots to diagnose calibration; final test calibration is evaluated, not repaired using test outcomes. Out-of-bag scores are secondary and do not replace the later-date validation set.

**Bayesian hierarchical logistic regression.** The statistical levels are:

| Level | Observational unit | Available information | Model role |
|---|---|---|---|
| 1 | A game | Binary victory and the four 15-minute differences | Bernoulli response with a logistic link and common predictor coefficients |
| 2 | A game patch | Text-preserved patch identifier | Patch-specific intercept and gold slope drawn from common distributions |

The full Korean 2024 refit sample contains 12 patches with 21-70 games per patch. The initial training subset has eight patches and validation has four additional patches. Patch is a grouping index, not a measured explanation of which balance change caused a difference. No fabricated patch-level balance variable is assumed. Teams cross patches and are not nested within patches; leagues are held-out domains, not an additional random-effect level estimated from two leagues.

A starting `brms` formula is `y ~ gold15_z + kills15_z + experience15_z + creep15_z + (1 + gold15_z || patch)`. Common slopes use zero-centered Normal(0, 1) priors on standardized predictors, the overall intercept uses Normal(0, 1.5), and patch standard deviations use Exponential(1) priors. Patch intercept and slope deviations are initially independent to avoid estimating an unnecessary covariance from few groups. These are starting prior choices to be checked through prior predictive simulation, not guarantees of appropriate shrinkage.

Fit four chains and inspect trace plots, rank-normalized R-hat, effective sample sizes, Monte Carlo uncertainty, and divergent transitions. Target R-hat below 1.01 and resolve important sampling problems before interpreting estimates. Check sensitivity to narrower and wider prior scales, and whether posterior replicated outcomes reproduce observed win frequencies by gold band and patch. Report 95 percent credible intervals for patch variation and conditional probabilities. Partial pooling can still leave wide intervals and depends on an approximate exchangeability assumption across chronologically ordered patches.

**New patches at prediction time.** None of the 2025 test patch codes occurs in the 2024 source set. For each posterior draw, draw an intercept and gold-slope deviation for each unseen patch from the fitted group distribution, compute game probabilities, and average probabilities over draws. Games sharing a new patch share its effect within each draw. The same predictive treatment is required for the new validation patches. Do not estimate new patch effects from held-out outcomes, substitute fitted 2025 effects, or silently treat a zero group effect as the same thing as integrating over its uncertainty. In `brms`, use the documented new-level prediction mechanism and posterior expected probabilities; replicated binary outcomes serve posterior predictive checks, not probability scoring. See [brms prediction documentation](https://paulbuerkner.com/brms/reference/posterior_predict.brmsfit.html).

The common predictor comparison includes all three supervised model families. The Bayesian model additionally uses patch grouping, so its contrast with pooled regression assesses both hierarchical structure and the prior assumptions. It is not a claim that every difference is caused by choosing Bayesian rather than frequentist inference.

## Supporting clustering

Use k-means only as an exploratory description of source-league early states. Standardize the same four predictors using the training subset. Compare two to four clusters using silhouette width, profiles, and week-block resampling stability, without win/loss labels. Examine whether profiles persist in the source validation subset; after selecting a rule, refit on the source refit set only. Any external assignment uses frozen centers and scaling. Similar-looking clusters or different group win rates do not prove distinct strategies or supply independent predictive information beyond their input features. Weak separation is an acceptable descriptive result. This component should not expand the three core questions into a separate collection of clustering hypotheses.

## Evaluation and dependence

The primary comparison measure is test log loss; also report Brier score and calibration curves with group sizes. These measure probability quality, not only the frequency of correct hard classifications. A reference forecast uses the source-refit win proportion, never the test-set prevalence. The area under the receiver operating characteristic curve can be a supplementary measure, written in full before any abbreviation is introduced.

For each test set, compare all frozen models on identical games. Resample entire calendar weeks 1,000 times, keeping predictions paired across models. This accounts for some short-term dependence and provides uncertainty for score differences conditional on the fitted models. Report the limitation that repeated teams can span weeks. A two-week-block sensitivity can show whether conclusions depend strongly on block length. The tests each have 27 observed weeks; the block count limits precision. Do not claim that this bootstrap covers all training, model-selection, or long-term dependence uncertainty.

For regression coefficient or probability intervals, week-block refits of the source data can assess some sensitivity to dependence. Bayesian patch grouping does not by itself account for all within-team or within-series dependence. Check residual summaries by team and week; if remaining dependence is substantial, describe the limitation and assess a predeclared week-effect sensitivity on the source data before final testing. Sampling convergence is computational evidence, not proof of an adequate statistical model.

Report each test set broken down by patch as well as pooled. This decomposition is declared here, before any test outcome is seen, and it exists for interpretation only: it must never change a model, a calibration, or which patches get reported. A shortfall spread evenly across patches points to a broad change in rosters, playstyle or competition, while one concentrated in particular patches is more consistent with version effects, and the within-source patch variation estimated for the second question calibrates which reading is plausible. The Korean 2025 set averages about 43 games per patch and the European set about 26, so per-patch intervals will be wide. This is descriptive decomposition, not a hypothesis test, and the pooled scores remain the primary comparison.

## Generalizability and final report

Good performance on the Korean 2025 test supports limited time transfer. Similar probability quality on the external 2025 test supports limited cross-league transfer under this saved coverage. Different compositions of teams, patch schedules, match formats, and missing records can contribute to gaps. This applies to the time transfer as much as to the regional one: a shortfall on the Korean 2025 test mixes version change with roster turnover and shifts in playstyle, and this design does not attribute it to any one of them. Comparing the two 2025 tests isolates only the additional regional component, conditional on the year. Neither test establishes causal regional differences or guarantees future accuracy. The framework can be adapted to another league or game only after defining comparable early resource and outcome variables and conducting a new external validation; fitted coefficients and cluster centers are not automatically transferable.

The final report will use Introduction, Data, Methods, Results, and Discussion/Conclusions. Results remain unwritten until analysis is carried out. Expected findings are hypotheses, and the report will include weak clusters, uncertain patch differences, or a random forest performing worse than simpler regression if observed.

## Source status and further data

The saved raw-file manifest and the structural audit remain the source of the reported counts. The live ChainCC download page has changed since the saved snapshot, so any later refresh requires a separate version and a new audit. Oracle's Elixir is a planned source check, not an already acquired independent dataset. Match duplicate records before combining sources. Earlier 2023 data are no longer part of the required primary plan; any later historical supplement must preserve the external-test separation.

Primary tools are R `stats`, `cluster`, `brms`, `ranger`, and `ggplot2`. The existing source audit has run; regression, clustering, posterior simulation, and test scoring have not.
