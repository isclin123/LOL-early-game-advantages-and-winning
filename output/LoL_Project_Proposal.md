# Early Game Advantages and Winning in League of Legends

Sicheng Yi

**Introduction.** In professional League of Legends, an early lead does not guarantee a win. Estimating win probabilities can help describe which advantages matter and whether a model remains useful when the competition changes. I will focus on three questions: (1) How are 15-minute advantages related to winning? (2) Does the gold-win relationship vary across game patches? (3) Do models trained in Korea predict games in another league and year?

**Data and Outcome.** The saved ChainCC sample contains 1,637 checked 2024-2025 games from League of Legends Champions Korea and the regional championship for Europe, the Middle East and Africa [1, 2]. Each row pairs both teams in one game. The outcome is final blue-side victory (1 = win, 0 = loss); models estimate its probability at 15 minutes. Predictors are blue-minus-red gold, kills, experience, and creep score (minions and monsters killed). Date, patch (game version), league, and team identifiers describe context. I will check missing fields and duplicates against Oracle's Elixir where available [3].

**Models.** Using R, I will compare logistic regression, random forests, and Bayesian hierarchical logistic regression with the same early predictors. In the hierarchical model, games form level 1, with their early statistics; patches form level 2, identified by patch codes, with varying intercepts and gold slopes. Patch membership is the available group-level information. K-means on standardized early statistics will provide supporting descriptions, excluding outcomes from clustering.

**Training Validation and Testing.** I will train on Korean games from January-June 2024 (313), validate on July-September (169), then refit on all 482 games and freeze the models. Separate 2025 tests use 555 Korean games for temporal transfer and 306 European games for cross-league transfer. European 2024 games remain outside model development. Preprocessing is fitted on training data; test outcomes never guide tuning. Bayesian forecasts for unseen patches will average over new patch effects.

**Model Checks.** I will examine separation, residual patterns, and influential games for regression; prior sensitivity, chain convergence, and posterior predictive checks for Bayesian models; and silhouette scores and resampling stability for clustering. Validation log loss will guide forest tuning. Test comparisons will report log loss, Brier score, and calibration, with week-block bootstrap intervals to reflect some within-week dependence.

**Expected Contribution and Limits.** I expect larger early leads to be associated with more wins, but complex models may not predict better. Performance on both test sets will assess limited transfer across years and leagues; other games require compatible variables and new validation. Repeated teams, small patch groups, and missing coverage limit conclusions, and associations are not causal. The final report will include introduction, data, methods, results, and discussion/conclusions.



[1] ChainCC. Data and downloads: https://chaincc.lol/free/data

[2] ChainCC. Data sources and methodology: https://chaincc.lol/about/methodology

[3] Oracle's Elixir. Planned source for checks: https://oracleselixir.com/tools/downloads
