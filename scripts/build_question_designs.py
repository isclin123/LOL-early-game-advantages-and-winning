"""Build the companion research designs; does not fit statistical models."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
content = json.loads((ROOT / 'proposal_content.json').read_text(encoding='utf-8'))
if content.get('revision') == 'teacher_feedback_2026-10-20':
    raise SystemExit('Historical question bank retained; current proposal has three core questions. See 04_analysis_plan.md.')
# Level, purpose, variables, methods/tools, expectation, limitations, keywords, four sentences.
designs = [
    [
        '1 Foundation', 'Describe side balance across leagues.',
        'Binary blue-side result; league; actual year for descriptive breakdowns; prior team-strength difference for an adjusted check.',
        'Estimate each league\'s blue-side win proportion and their difference with calendar-week block bootstrap confidence intervals. Plot with ggplot2; use stats::glm with league and prior strength for an adjusted sensitivity analysis.',
        'A modest difference is possible; similar rates would also be useful. No direction between leagues is assumed.',
        'Raw fields are present; prior strength must be derived from earlier matches. Team quality and side-selection rules prevent a causal interpretation.',
        'League of Legends, ChainCC, blue side, league, win proportion, bootstrap',
        [
            'I will compare blue-side win rates in LCK and LEC to describe side balance.',
            'I will use match outcome, league, and date from paired ChainCC games.',
            'I will estimate proportions and week-block bootstrap confidence intervals in R, with an adjusted regression as a sensitivity check.',
            'I expect a modest difference is possible, but similar rates would also help describe these leagues.'
        ]
    ],
    [
        '1 Foundation', 'Estimate comeback frequency under a clear deficit definition.',
        'Absolute golddiffat15 in gold; derived binary trailing_win; league and date. Restrict to games with an absolute deficit of at least 2,000 gold and count each game once.',
        'Report comeback counts and proportions overall and in deficit bands [2000, 4000) and [4000, infinity). Use week-block bootstrap intervals and ggplot2.',
        'Larger deficits may be followed by fewer comebacks; no exact rate is assumed.',
        'The structural check identifies 562 qualifying games; comeback event counts have not been examined. Small or zero-event groups need transparent counts and boundary-aware uncertainty; a degenerate bootstrap interval is not evidence of certainty.',
        'League of Legends, ChainCC, comeback, gold deficit, proportions, uncertainty',
        [
            'I will estimate how often teams win after trailing by at least 2,000 gold at 15 minutes.',
            'I will identify the trailing team and its final outcome from the paired ChainCC records.',
            'I will report comeback counts, proportions, and week-block bootstrap intervals in R.',
            'I expect larger deficits to be associated with fewer comebacks, although small groups may give imprecise estimates.'
        ]
    ],
    [
        '2 Regression', 'Estimate the economy-outcome relationship and examine its shape.',
        'Binary blue-side win; golddiffat15 in 1,000 gold; league and prior team-strength difference.',
        'Compare logistic regression with a linear gold term and a natural cubic spline with 3 degrees of freedom, using stats and splines. Compare rolling-validation log loss within 2024 and plot block-bootstrap probability curves.',
        'Larger leads should relate to higher winning probabilities; a spline may or may not improve prediction over a linear log-odds term.',
        'Gold is observed rather than assigned. Tail estimates may be unstable. A sigmoid probability curve alone does not establish nonlinearity on the log-odds scale.',
        'League of Legends, ChainCC, gold lead, logistic regression, natural spline, nonlinearity',
        [
            'I will study whether the relationship between a 15-minute gold lead and winning needs a nonlinear term.',
            'I will use gold difference, match outcome, league, and prior team strength from the ChainCC sample.',
            'I will compare linear and spline logistic models in R and report probability curves with uncertainty.',
            'I expect winning probability to increase with the lead, but a flexible curve may not improve prediction over a simpler model.'
        ]
    ],
    [
        '2 Regression', 'Assess information beyond economy while addressing correlated predictors.',
        'Binary win; golddiffat15, killdiffat15, xpdiffat15, and csdiffat15; league and prior strength. Units are gold, kills, experience points, and creep score.',
        'Add kills, XP, and CS individually and jointly to the gold-and-context logistic model. Compare conditional estimates, their uncertainty, and rolling-validation log loss using stats, splines, and ggplot2.',
        'Extra indicators may add little after gold is included; their joint contribution may be more stable than individual coefficients.',
        'Required snapshots exist. Collinearity can destabilize individual coefficients; assess the indicators jointly and report uncertainty rather than interpret coefficients as causal importance.',
        'League of Legends, ChainCC, early indicators, multivariable regression, collinearity, added information',
        [
            'I will examine whether kills, experience, and CS provide information about winning beyond gold.',
            'I will use their 15-minute differences, match outcomes, and shared context variables from ChainCC.',
            'I will compare multivariable logistic models in R and examine coefficient uncertainty and predictive performance.',
            'I expect the added information may be small, which would show how much of the early advantage gold already captures.'
        ]
    ],
    [
        '2 Regression', 'Study gaining ground at a similar starting position.',
        'Binary win; golddiffat10 and goldgain10to15 = golddiffat15 - golddiffat10, scaled in thousands; league and prior strength.',
        'Fit logistic regression with the initial gold gap and change, using a spline for the initial gap where supported; stats, splines, and ggplot2.',
        'Gaining ground may be associated with more wins at a similar initial gap.',
        'Both snapshots exist. Do not include the initial gap, final gap, and their change together because of exact linear dependence. Change is a re-expression of the snapshots, not an independent measure of psychological momentum.',
        'League of Legends, ChainCC, gold change, initial advantage, logistic regression, winning',
        [
            'I will study whether gaining ground between 10 and 15 minutes is associated with winning.',
            'I will calculate the change in gold difference and account for the initial gap, league, and prior team strength.',
            'I will fit logistic regression in R using the initial gap and change without also including the final gap.',
            'I expect gaining ground to be associated with more wins, but this will not establish a causal momentum effect.'
        ]
    ],
    [
        '3 Multivariate analysis', 'Discover early match states without using outcomes.',
        'The four standardized blue-minus-red gold, kill, XP, and CS differences at 15 minutes in the 776 checked 2024 games. Exclude outcome, team identity, league, and patch from clustering features.',
        'Use stats::kmeans with K = 2-5 and multiple starts. Assess cluster::silhouette, minimum group sizes, and week-block resampling stability. Use stats::prcomp for a PCA visualization only.',
        'Broad balanced or lead-related patterns may appear, but no natural number or type of groups is assumed.',
        'Four numerical features keep computation modest. Correlated indicators may mainly describe one advantage gradient. Scaling and outliers matter; weak separation is an acceptable finding. Clusters describe match states, not fixed team strategies.',
        'League of Legends, ChainCC, match states, k-means, silhouette, cluster stability',
        [
            'I will explore whether 15-minute match statistics form stable groups of early-game states.',
            'I will use standardized gold, kill, experience, and CS differences from 2024 ChainCC games without using final outcomes.',
            'I will apply k-means in R and assess the groups with silhouette scores and resampling stability.',
            'I expect broad advantage patterns may appear, but weak separation would suggest that the data form a continuous range instead.'
        ]
    ],
    [
        '3 Multivariate analysis', 'Check whether discovered groups describe later matches.',
        'The same four 15-minute differences in 861 checked 2025 games; frozen 2024 means, scales, and cluster centers; cluster label, year, and binary outcome for later summaries.',
        'Assign later games to their nearest frozen center. Compare group sizes, silhouettes, distances to centers, and profiles; then report cluster win rates with week-block intervals using base R, cluster, and ggplot2.',
        'Strong-lead groups may have higher win rates; group composition or separation may change in 2025.',
        'Every game can be assigned to a center, so assignment alone is not evidence of transfer. Outcomes must not determine K or labels. Group win-rate differences may simply reflect the gold difference already used for clustering.',
        'League of Legends, ChainCC, frozen clusters, temporal transfer, win rates, stability',
        [
            'I will test whether the early-game groups found in 2024 remain useful for describing 2025 matches.',
            'I will assign 2025 ChainCC games using the same scaling and cluster centers, then examine their outcomes.',
            'I will compare group profiles and separation and estimate group win rates in R.',
            'I expect some patterns may continue, but weaker separation or changing profiles would show limits to their transfer.'
        ]
    ],
    [
        '4 Bayesian inference', 'Estimate variation across patches with partial pooling.',
        'Binary blue-side win; standardized 15-minute gold difference and prior-strength difference; league as a fixed effect; 26 text-preserved patch codes as groups.',
        'Use brms Bayesian hierarchical logistic regression with patch-specific intercepts and gold slopes. Specify regularizing priors, compare with complete pooling, and report posterior intervals. Check prior sensitivity, posterior predictions, R-hat, effective sample sizes, and sampler diagnostics.',
        'Small patches may be influenced more strongly by shared information. The amount of variation and resulting precision are unknown.',
        'Analyze the full cohort retrospectively after predictive recipes are frozen and evaluated. Sparse patches can remain uncertain; partial pooling relies on assumptions. Date, teams, and format confound patches. Add a week-level effect as a dependence sensitivity check.',
        'League of Legends, ChainCC, patch variation, Bayesian logistic regression, partial pooling, credible intervals',
        [
            'I will study how the relationship between a gold lead and winning varies across game patches.',
            'I will use gold difference, outcome, league, prior team strength, and patch from the checked ChainCC games.',
            'I will fit a Bayesian hierarchical logistic model in R and examine partial pooling, prior sensitivity, and posterior predictive checks.',
            'I expect estimates for small patches to depend more on shared information, while wide credible intervals would show remaining uncertainty.'
        ]
    ],
    [
        '5 Predictive modeling', 'Test whether flexible nonlinear relationships and interactions improve future probability prediction.',
        'Binary win; 15-minute gold, kill, XP, and CS differences; league and pregame Elo difference. Use identical 2024 development and 2025 test rows for all models.',
        'Compare spline logistic regression (stats, splines) with probability random forests (ranger). Tune only with rolling chronological validation in 2024. Evaluate 2025 log loss, Brier score, AUC, and calibration, with paired week-block bootstrap comparisons.',
        'Random forests may capture interactions, but they are not assumed to outperform logistic regression.',
        'There are 776 training games, so use a small tuning grid and constrained trees. Overfitting and repeated teams limit generalization. Poorer performance of a complex model is a useful result, not a reason to change the test set.',
        'League of Legends, ChainCC, logistic regression, random forest, temporal validation, calibration',
        [
            'I will examine whether random forests improve win prediction over logistic regression.',
            'I will use the same 15-minute statistics and context from ChainCC, training on 2024 games and testing on 2025 games.',
            'I will tune models with rolling validation in R and compare log loss, Brier score, AUC, and calibration on the fixed test year.',
            'I expect flexible models may help, but similar or worse performance would support using a simpler model.'
        ]
    ],
    [
        '5 Predictive modeling', 'Separate the value of later information from the choice of model.',
        'Matched gold, kill, XP, and CS differences at 10 or 15 minutes, identical league and prior-strength controls, and the same games and outcomes for each model.',
        'Fit the same two model families at each time with identical splits and tuning budgets. Reuse Q9\'s 15-minute models. Report paired test log-loss and Brier differences with week-block bootstrap intervals; use AUC and calibration as supporting measures.',
        'Fifteen-minute forecasts may improve, but the amount of improvement may differ by model.',
        'Both snapshots are available; this adds three earlier-time models, not a new dataset. Later forecasts leave less advance notice. Do not choose a favored model-time pair from the test results and claim it had an independent final evaluation.',
        'League of Legends, ChainCC, prediction time, machine learning, paired comparison, log loss',
        [
            'I will measure how prediction performance changes when using 15-minute statistics instead of 10-minute statistics.',
            'I will use the same ChainCC games and matched types of predictors for each time point.',
            'I will compare logistic regression and random forests in R using paired test scores and week-block bootstrap intervals.',
            'I expect later forecasts to improve, but the gain will be considered alongside their shorter prediction lead time.'
        ]
    ]
]
assert len(designs) == len(content['questions']) == 10
lines = [
    '# Ten Research Questions for League of Legends', '',
    'The project studies early advantages, match patterns, and win prediction. All questions use the checked ChainCC sample of 1,637 available LCK and LEC games dated 2024-2025, paired to one blue-side row per game. R is the analysis tool. All expected results are hypotheses, not findings.', '',
    'Sources: [ChainCC data](https://chaincc.lol/free/data), [source methodology](https://chaincc.lol/about/methodology), and [Oracle\'s Elixir](https://oracleselixir.com/tools/downloads), a planned source for checks whose files have not yet been obtained. Shared data definitions and validation rules are in `01_data_and_methods.md`.', '',
    '| Level | Questions | Purpose |', '|---|---|---|',
    '| 1 Foundation | Q1-Q2 | Proportions and uncertainty |',
    '| 2 Regression | Q3-Q5 | Nonlinear and conditional relationships |',
    '| 3 Multivariate analysis | Q6-Q7 | Clustering and temporal transfer |',
    '| 4 Bayesian inference | Q8 | Patch variation and partial pooling |',
    '| 5 Predictive modeling | Q9-Q10 | Statistical learning and temporal validation |', ''
]
for i, (question, card) in enumerate(zip(content['questions'], designs), 1):
    level, purpose, variables, methods, expectation, limitations, keywords, sentences = card
    assert len(sentences) == 4 and all(s.endswith('.') for s in sentences)
    lines += [f'## Q{i} {question}', '',
              f'- **Purpose and level:** {purpose} {level}.',
              '- **Dataset and unit:** Checked ChainCC team data, using the shared source links above; one paired game per observation, with the subset stated below.',
              f'- **Variables:** {variables}',
              f'- **Methods and R tools:** {methods}',
              f'- **Expected results:** {expectation}',
              f'- **Feasibility and limitations:** {limitations}',
              f'- **Keywords:** {keywords}.', '', '**Four sentence summary**', '']
    lines += [f'{j}. {sentence}' for j, sentence in enumerate(sentences, 1)] + ['']
lines += ['## How the questions fit together', '',
          'Q1-Q2 establish basic patterns; Q3-Q5 build interpretable regressions; Q6-Q7 examine multivariate states and their transfer; Q8 studies uncertainty across patches; Q9-Q10 compare predictive models and information times. Regression, clustering, Bayesian analysis, and machine learning are all planned parts of one project, sharing data and checks.', '',
          'All ten questions appear in the one-page proposal. This companion retains the complete designs, keywords, and forty summary sentences. No semester schedule is included. Full course lectures and the assignment rubric were not available in this folder; these methods are graduate-level design choices rather than methods confirmed taught by the instructor.', '']
(ROOT / '02_ten_research_questions.md').write_text('\n'.join(lines), encoding='utf-8')
print('Wrote 10 aligned research designs and 40 summary sentences.')
