# Data readiness audit

Audit date: 2026-10-20. No models fitted. Validation and test outcomes were not summarized or associated with predictors.

## Frozen source and derived-data consistency
   raw_duplicate_game_side_keys      raw_games_without_two_rows 
                              0                               0 
         missing_required_cells               nonbinary_results 
                              0                               0 
noncomplementary_paired_results              nonpositive_gold15 
                              0                               0 
  no_15minute_snapshot_duration    inconsistent_gold_difference 
                              0                               0 
    inconsistent_paired_context         same_team_on_both_sides 
                              0                               0 
   kills_exceed_opposing_deaths     repeated_natural_match_keys 
                              0                               0 
        derived_gold_mismatches         derived_kill_mismatches 
                              0                               0 
  derived_experience_mismatches        derived_creep_mismatches 
                              0                               0 
       nonopposite_golddiffat15          nonopposite_xpdiffat15 
                              0                               0 
         nonopposite_csdiffat15 
                              0 
Nonfinite feature values:
golddiffat15 killdiffat15   xpdiffat15   csdiffat15 
           0            0            0            0 

## Partition support
                          part games teams patches weeks missing_features
      train_korea_2024_jan_jun   313    10       8    15                0
 validation_korea_2024_jul_sep   169    10       4     9                0
      test_temporal_korea_2025   555    10      13    27                0
     test_external_europe_2025   306    11      12    27                0
            unused_europe_2024   294    10       8    23                0
 constant_features
                 0
                 0
                 0
                 0
                 0

The final source refit is training plus validation (482 games), not an extra independent partition.
All partitions are disjoint and together match the saved cohort.

## Initial training subset only
Outcome counts:

blue_loss  blue_win 
      152       161 
Predictor ranges and variation:
        field   min  max          sd distinct
 golddiffat15 -6099 5977 2250.103064      304
 killdiffat15    -8    8    2.709767       16
   xpdiffat15 -3782 5625 1713.522212      299
   csdiffat15  -120   95   35.792115      129
Linear design rank including intercept: 5 of 5
Standardized design condition number: 6.8965
Smaller class count per linear-model coefficient including intercept: 30.4
This ratio is a descriptive workload check, not a sample-size sufficiency theorem or power calculation.
Training predictor correlation:
             golddiffat15 killdiffat15 xpdiffat15 csdiffat15
golddiffat15        1.000        0.813      0.834      0.702
killdiffat15        0.813        1.000      0.741      0.326
xpdiffat15          0.834        0.741      1.000      0.708
csdiffat15          0.702        0.326      0.708      1.000

## Source refit patch support (no outcome grouping)
 patch games gold_distinct gold_negative gold_positive
 14.01    70            70            39            31
 14.02    21            21             9            12
 14.03    48            48            21            27
 14.04    49            48            21            28
 14.05    22            22            14             8
 14.06    32            32            14            18
 14.11    26            26            12            14
 14.12    45            45            18            27
 14.13    46            46            21            25
 14.14    46            46            21            25
 14.15    46            46            20            26
 14.16    31            31            13            18
Patch groups: 12
Patch count range: 21 to 70
Random-slope precision and between-patch variance remain uncertain with this number of groups.

## Independent verification boundary
Internal agreement does not independently establish correct timestamps, definitions, completeness, or event measurement.
No test scores, test win rates, or predictor-outcome associations were computed for this audit.
