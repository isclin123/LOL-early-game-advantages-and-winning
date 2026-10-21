# Ten Research Questions for League of Legends

The project studies early advantages, match patterns, and win prediction. All questions use the checked ChainCC sample of 1,637 available LCK and LEC games dated 2024-2025, paired to one blue-side row per game. R is the analysis tool. All expected results are hypotheses, not findings.

Sources: [ChainCC data](https://chaincc.lol/free/data), [source methodology](https://chaincc.lol/about/methodology), and [Oracle's Elixir](https://oracleselixir.com/tools/downloads), a planned source for checks whose files have not yet been obtained. Shared data definitions and validation rules are in `01_data_and_methods.md`.

| Level | Questions | Purpose |
|---|---|---|
| 1 Foundation | Q1-Q2 | Proportions and uncertainty |
| 2 Regression | Q3-Q5 | Nonlinear and conditional relationships |
| 3 Multivariate analysis | Q6-Q7 | Clustering and temporal transfer |
| 4 Bayesian inference | Q8 | Patch variation and partial pooling |
| 5 Predictive modeling | Q9-Q10 | Statistical learning and temporal validation |

## Q1 How do blue-side win rates differ between LCK and LEC?

- **Purpose and level:** Describe side balance across leagues. 1 Foundation.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Binary blue-side result; league; actual year for descriptive breakdowns; prior team-strength difference for an adjusted check.
- **Methods and R tools:** Estimate each league's blue-side win proportion and their difference with calendar-week block bootstrap confidence intervals. Plot with ggplot2; use stats::glm with league and prior strength for an adjusted sensitivity analysis.
- **Expected results:** A modest difference is possible; similar rates would also be useful. No direction between leagues is assumed.
- **Feasibility and limitations:** Raw fields are present; prior strength must be derived from earlier matches. Team quality and side-selection rules prevent a causal interpretation.
- **Keywords:** League of Legends, ChainCC, blue side, league, win proportion, bootstrap.

**Four sentence summary**

1. I will compare blue-side win rates in LCK and LEC to describe side balance.
2. I will use match outcome, league, and date from paired ChainCC games.
3. I will estimate proportions and week-block bootstrap confidence intervals in R, with an adjusted regression as a sensitivity check.
4. I expect a modest difference is possible, but similar rates would also help describe these leagues.

## Q2 How often do teams win after trailing by at least 2,000 gold at 15 minutes?

- **Purpose and level:** Estimate comeback frequency under a clear deficit definition. 1 Foundation.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Absolute golddiffat15 in gold; derived binary trailing_win; league and date. Restrict to games with an absolute deficit of at least 2,000 gold and count each game once.
- **Methods and R tools:** Report comeback counts and proportions overall and in deficit bands [2000, 4000) and [4000, infinity). Use week-block bootstrap intervals and ggplot2.
- **Expected results:** Larger deficits may be followed by fewer comebacks; no exact rate is assumed.
- **Feasibility and limitations:** The structural check identifies 562 qualifying games; comeback event counts have not been examined. Small or zero-event groups need transparent counts and boundary-aware uncertainty; a degenerate bootstrap interval is not evidence of certainty.
- **Keywords:** League of Legends, ChainCC, comeback, gold deficit, proportions, uncertainty.

**Four sentence summary**

1. I will estimate how often teams win after trailing by at least 2,000 gold at 15 minutes.
2. I will identify the trailing team and its final outcome from the paired ChainCC records.
3. I will report comeback counts, proportions, and week-block bootstrap intervals in R.
4. I expect larger deficits to be associated with fewer comebacks, although small groups may give imprecise estimates.

## Q3 Is the relationship between a 15-minute gold lead and winning nonlinear?

- **Purpose and level:** Estimate the economy-outcome relationship and examine its shape. 2 Regression.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Binary blue-side win; golddiffat15 in 1,000 gold; league and prior team-strength difference.
- **Methods and R tools:** Compare logistic regression with a linear gold term and a natural cubic spline with 3 degrees of freedom, using stats and splines. Compare rolling-validation log loss within 2024 and plot block-bootstrap probability curves.
- **Expected results:** Larger leads should relate to higher winning probabilities; a spline may or may not improve prediction over a linear log-odds term.
- **Feasibility and limitations:** Gold is observed rather than assigned. Tail estimates may be unstable. A sigmoid probability curve alone does not establish nonlinearity on the log-odds scale.
- **Keywords:** League of Legends, ChainCC, gold lead, logistic regression, natural spline, nonlinearity.

**Four sentence summary**

1. I will study whether the relationship between a 15-minute gold lead and winning needs a nonlinear term.
2. I will use gold difference, match outcome, league, and prior team strength from the ChainCC sample.
3. I will compare linear and spline logistic models in R and report probability curves with uncertainty.
4. I expect winning probability to increase with the lead, but a flexible curve may not improve prediction over a simpler model.

## Q4 Do kills, experience, and CS add information beyond gold at 15 minutes?

- **Purpose and level:** Assess information beyond economy while addressing correlated predictors. 2 Regression.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Binary win; golddiffat15, killdiffat15, xpdiffat15, and csdiffat15; league and prior strength. Units are gold, kills, experience points, and creep score.
- **Methods and R tools:** Add kills, XP, and CS individually and jointly to the gold-and-context logistic model. Compare conditional estimates, their uncertainty, and rolling-validation log loss using stats, splines, and ggplot2.
- **Expected results:** Extra indicators may add little after gold is included; their joint contribution may be more stable than individual coefficients.
- **Feasibility and limitations:** Required snapshots exist. Collinearity can destabilize individual coefficients; assess the indicators jointly and report uncertainty rather than interpret coefficients as causal importance.
- **Keywords:** League of Legends, ChainCC, early indicators, multivariable regression, collinearity, added information.

**Four sentence summary**

1. I will examine whether kills, experience, and CS provide information about winning beyond gold.
2. I will use their 15-minute differences, match outcomes, and shared context variables from ChainCC.
3. I will compare multivariable logistic models in R and examine coefficient uncertainty and predictive performance.
4. I expect the added information may be small, which would show how much of the early advantage gold already captures.

## Q5 Does gold gain from 10 to 15 minutes relate to winning after accounting for the initial gap?

- **Purpose and level:** Study gaining ground at a similar starting position. 2 Regression.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Binary win; golddiffat10 and goldgain10to15 = golddiffat15 - golddiffat10, scaled in thousands; league and prior strength.
- **Methods and R tools:** Fit logistic regression with the initial gold gap and change, using a spline for the initial gap where supported; stats, splines, and ggplot2.
- **Expected results:** Gaining ground may be associated with more wins at a similar initial gap.
- **Feasibility and limitations:** Both snapshots exist. Do not include the initial gap, final gap, and their change together because of exact linear dependence. Change is a re-expression of the snapshots, not an independent measure of psychological momentum.
- **Keywords:** League of Legends, ChainCC, gold change, initial advantage, logistic regression, winning.

**Four sentence summary**

1. I will study whether gaining ground between 10 and 15 minutes is associated with winning.
2. I will calculate the change in gold difference and account for the initial gap, league, and prior team strength.
3. I will fit logistic regression in R using the initial gap and change without also including the final gap.
4. I expect gaining ground to be associated with more wins, but this will not establish a causal momentum effect.

## Q6 What early-game patterns can clustering identify from 15-minute statistics?

- **Purpose and level:** Discover early match states without using outcomes. 3 Multivariate analysis.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** The four standardized blue-minus-red gold, kill, XP, and CS differences at 15 minutes in the 776 checked 2024 games. Exclude outcome, team identity, league, and patch from clustering features.
- **Methods and R tools:** Use stats::kmeans with K = 2-5 and multiple starts. Assess cluster::silhouette, minimum group sizes, and week-block resampling stability. Use stats::prcomp for a PCA visualization only.
- **Expected results:** Broad balanced or lead-related patterns may appear, but no natural number or type of groups is assumed.
- **Feasibility and limitations:** Four numerical features keep computation modest. Correlated indicators may mainly describe one advantage gradient. Scaling and outliers matter; weak separation is an acceptable finding. Clusters describe match states, not fixed team strategies.
- **Keywords:** League of Legends, ChainCC, match states, k-means, silhouette, cluster stability.

**Four sentence summary**

1. I will explore whether 15-minute match statistics form stable groups of early-game states.
2. I will use standardized gold, kill, experience, and CS differences from 2024 ChainCC games without using final outcomes.
3. I will apply k-means in R and assess the groups with silhouette scores and resampling stability.
4. I expect broad advantage patterns may appear, but weak separation would suggest that the data form a continuous range instead.

## Q7 Do the 2024 clusters remain useful in 2025, and how do their win rates differ?

- **Purpose and level:** Check whether discovered groups describe later matches. 3 Multivariate analysis.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** The same four 15-minute differences in 861 checked 2025 games; frozen 2024 means, scales, and cluster centers; cluster label, year, and binary outcome for later summaries.
- **Methods and R tools:** Assign later games to their nearest frozen center. Compare group sizes, silhouettes, distances to centers, and profiles; then report cluster win rates with week-block intervals using base R, cluster, and ggplot2.
- **Expected results:** Strong-lead groups may have higher win rates; group composition or separation may change in 2025.
- **Feasibility and limitations:** Every game can be assigned to a center, so assignment alone is not evidence of transfer. Outcomes must not determine K or labels. Group win-rate differences may simply reflect the gold difference already used for clustering.
- **Keywords:** League of Legends, ChainCC, frozen clusters, temporal transfer, win rates, stability.

**Four sentence summary**

1. I will test whether the early-game groups found in 2024 remain useful for describing 2025 matches.
2. I will assign 2025 ChainCC games using the same scaling and cluster centers, then examine their outcomes.
3. I will compare group profiles and separation and estimate group win rates in R.
4. I expect some patterns may continue, but weaker separation or changing profiles would show limits to their transfer.

## Q8 How does the gold-win relationship vary across patches in a Bayesian hierarchical model?

- **Purpose and level:** Estimate variation across patches with partial pooling. 4 Bayesian inference.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Binary blue-side win; standardized 15-minute gold difference and prior-strength difference; league as a fixed effect; 26 text-preserved patch codes as groups.
- **Methods and R tools:** Use brms Bayesian hierarchical logistic regression with patch-specific intercepts and gold slopes. Specify regularizing priors, compare with complete pooling, and report posterior intervals. Check prior sensitivity, posterior predictions, R-hat, effective sample sizes, and sampler diagnostics.
- **Expected results:** Small patches may be influenced more strongly by shared information. The amount of variation and resulting precision are unknown.
- **Feasibility and limitations:** Analyze the full cohort retrospectively after predictive recipes are frozen and evaluated. Sparse patches can remain uncertain; partial pooling relies on assumptions. Date, teams, and format confound patches. Add a week-level effect as a dependence sensitivity check.
- **Keywords:** League of Legends, ChainCC, patch variation, Bayesian logistic regression, partial pooling, credible intervals.

**Four sentence summary**

1. I will study how the relationship between a gold lead and winning varies across game patches.
2. I will use gold difference, outcome, league, prior team strength, and patch from the checked ChainCC games.
3. I will fit a Bayesian hierarchical logistic model in R and examine partial pooling, prior sensitivity, and posterior predictive checks.
4. I expect estimates for small patches to depend more on shared information, while wide credible intervals would show remaining uncertainty.

## Q9 Do random forests predict wins better than logistic regression?

- **Purpose and level:** Test whether flexible nonlinear relationships and interactions improve future probability prediction. 5 Predictive modeling.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Binary win; 15-minute gold, kill, XP, and CS differences; league and pregame Elo difference. Use identical 2024 development and 2025 test rows for all models.
- **Methods and R tools:** Compare spline logistic regression (stats, splines) with probability random forests (ranger). Tune only with rolling chronological validation in 2024. Evaluate 2025 log loss, Brier score, AUC, and calibration, with paired week-block bootstrap comparisons.
- **Expected results:** Random forests may capture interactions, but they are not assumed to outperform logistic regression.
- **Feasibility and limitations:** There are 776 training games, so use a small tuning grid and constrained trees. Overfitting and repeated teams limit generalization. Poorer performance of a complex model is a useful result, not a reason to change the test set.
- **Keywords:** League of Legends, ChainCC, logistic regression, random forest, temporal validation, calibration.

**Four sentence summary**

1. I will examine whether random forests improve win prediction over logistic regression.
2. I will use the same 15-minute statistics and context from ChainCC, training on 2024 games and testing on 2025 games.
3. I will tune models with rolling validation in R and compare log loss, Brier score, AUC, and calibration on the fixed test year.
4. I expect flexible models may help, but similar or worse performance would support using a simpler model.

## Q10 How does prediction performance change from 10 to 15 minutes across these models?

- **Purpose and level:** Separate the value of later information from the choice of model. 5 Predictive modeling.
- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.
- **Variables:** Matched gold, kill, XP, and CS differences at 10 or 15 minutes, identical league and prior-strength controls, and the same games and outcomes for each model.
- **Methods and R tools:** Fit the same two model families at each time with identical splits and tuning budgets. Reuse Q9's 15-minute models. Report paired test log-loss and Brier differences with week-block bootstrap intervals; use AUC and calibration as supporting measures.
- **Expected results:** Fifteen-minute forecasts may improve, but the amount of improvement may differ by model.
- **Feasibility and limitations:** Both snapshots are available; this adds three earlier-time models, not a new dataset. Later forecasts leave less advance notice. Do not choose a favored model-time pair from the test results and claim it had an independent final evaluation.
- **Keywords:** League of Legends, ChainCC, prediction time, machine learning, paired comparison, log loss.

**Four sentence summary**

1. I will measure how prediction performance changes when using 15-minute statistics instead of 10-minute statistics.
2. I will use the same ChainCC games and matched types of predictors for each time point.
3. I will compare logistic regression and random forests in R using paired test scores and week-block bootstrap intervals.
4. I expect later forecasts to improve, but the gain will be considered alongside their shorter prediction lead time.

## How the questions fit together

Q1-Q2 establish basic patterns; Q3-Q5 build interpretable regressions; Q6-Q7 examine multivariate states and their transfer; Q8 studies uncertainty across patches; Q9-Q10 compare predictive models and information times. Regression, clustering, Bayesian analysis, and machine learning are all planned parts of one project, sharing data and checks.

All ten questions appear in the one-page proposal. This companion retains the complete designs, keywords, and forty summary sentences. No semester schedule is included. Full course lectures and the assignment rubric were not available in this folder; these methods are graduate-level design choices rather than methods confirmed taught by the instructor.
