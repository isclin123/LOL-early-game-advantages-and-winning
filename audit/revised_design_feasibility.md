# Revised design feasibility check

This check does not use outcomes to fit models or estimate associations.

## Numerical snapshot features
        field nonfinite distinct          sd
 golddiffat10         0     1332 1139.132931
 killdiffat10         0       17    1.773110
   xpdiffat10         0     1267  857.205257
   csdiffat10         0      127   22.636444
 golddiffat15         0     1464 2213.069570
 killdiffat15         0       21    2.845629
   xpdiffat15         0     1439 1649.611618
   csdiffat15         0      181   33.653306

## Proposed chronological folds within 2024
 fold train_games validation_games first_validation_week last_validation_week
    1         393              140            2024-04-08           2024-06-24
    2         533              134            2024-07-08           2024-07-29
    3         667              109            2024-08-05           2024-09-02

Observed 2024 weeks: 27
Observed 2025 weeks: 29
Patch groups: 26
Patch group size range: 9 to 115
Games meeting the Q2 deficit threshold: 562

Nonzero feature variation does not independently validate source measurements.
Outcome balance, model estimability, cluster separation, and Bayesian diagnostics remain future analysis checks.
