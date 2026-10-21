# Read-only structural checks for the revised design; no outcome modeling.
args <- grep('^--file=', commandArgs(FALSE), value = TRUE)
root <- dirname(dirname(normalizePath(sub('^--file=', '', args[[1]]))))
d <- readRDS(file.path(root, 'data/derived/eligible_games.rds'))
features <- c('golddiffat10', 'killdiffat10', 'xpdiffat10', 'csdiffat10',
              'golddiffat15', 'killdiffat15', 'xpdiffat15', 'csdiffat15')
stopifnot(all(features %in% names(d)), nrow(d) == 1637L,
          !anyDuplicated(d$game_id), all(vapply(d[features], is.numeric, logical(1))))
feature_checks <- data.frame(
  field = features,
  nonfinite = vapply(d[features], function(x) sum(!is.finite(x)), integer(1)),
  distinct = vapply(d[features], function(x) length(unique(x)), integer(1)),
  sd = vapply(d[features], sd, numeric(1)), row.names = NULL)
stopifnot(all(feature_checks$nonfinite == 0L), all(feature_checks$sd > 0))
d$year <- substr(d$date, 1, 4)
d$week <- as.character(cut(as.Date(substr(d$date, 1, 10)), breaks = 'weeks', start.on.monday = TRUE))
weeks <- sort(unique(d$week[d$year == '2024']))
boundaries <- floor(length(weeks) * c(.5, 2/3, 5/6, 1))
folds <- lapply(1:3, function(i) {
  train <- d$year == '2024' & d$week %in% weeks[seq_len(boundaries[i])]
  validation <- d$year == '2024' & d$week %in% weeks[seq.int(boundaries[i]+1, boundaries[i+1])]
  stopifnot(!any(train & validation), sum(train)>0, sum(validation)>0,
            length(unique(d$league[train])) == 2L,
            length(unique(d$league[validation])) == 2L)
  data.frame(fold = i, train_games = sum(train), validation_games = sum(validation),
             first_validation_week = min(d$week[validation]), last_validation_week = max(d$week[validation]))
})
patch_counts <- sort(table(d$patch))
report <- c('# Revised design feasibility check', '',
            'This check does not use outcomes to fit models or estimate associations.', '',
            '## Numerical snapshot features', capture.output(print(feature_checks, row.names=FALSE)), '',
            '## Proposed chronological folds within 2024', capture.output(print(do.call(rbind, folds), row.names=FALSE)), '',
            paste('Observed 2024 weeks:', length(weeks)),
            paste('Observed 2025 weeks:', length(unique(d$week[d$year == '2025']))),
            paste('Patch groups:', length(patch_counts)),
            paste('Patch group size range:', min(patch_counts), 'to', max(patch_counts)),
            paste('Games meeting the Q2 deficit threshold:', sum(abs(d$golddiffat15) >= 2000)), '',
            'Nonzero feature variation does not independently validate source measurements.',
            'Outcome balance, model estimability, cluster separation, and Bayesian diagnostics remain future analysis checks.')
writeLines(report, file.path(root, 'audit/revised_design_feasibility.md'))
cat(paste(report, collapse='\n'), '\n')
