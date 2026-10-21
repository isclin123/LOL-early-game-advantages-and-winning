# Deterministic training-only sample for source checking, not EDA or model fitting.
args <- grep('^--file=', commandArgs(FALSE), value=TRUE)
root <- dirname(dirname(normalizePath(sub('^--file=', '', args[[1]]))))
d <- readRDS(file.path(root, 'data/derived/eligible_games.rds'))
parts <- readRDS(file.path(root, 'audit/proposed_teacher_split_ids.rds'))
t <- d[d$game_id %in% parts$train_korea_2024_jan_jun, ]
t <- t[order(t$date, t$game_id), ]
stopifnot(nrow(t)==313L)
idx <- c(match(unique(t$patch), t$patch), which.min(t$golddiffat15),
         which.max(t$golddiffat15), head(which(t$csdiffat15==0 | t$xpdiffat15==0),1))
reason <- c(paste('First chronological game in patch', unique(t$patch)),
            'Minimum training gold difference', 'Maximum training gold difference',
            'First chronological game with zero CS or XP difference')
selected <- t[idx, c('game_id','date','league','patch','game_number','side',
  'team_name','team_id','red_team_name','red_team_id','result','gamelength',
  'goldat15','golddiffat15','killdiffat15','xpdiffat15','csdiffat15')]
selected$selection_reason <- reason
stopifnot(!anyDuplicated(selected$game_id), nrow(selected)==11L)
folder <- file.path(root, 'audit/source_check_2026-10-20')
dir.create(folder, recursive=TRUE, showWarnings=FALSE)
saveRDS(selected, file.path(folder, 'selected_training_games.rds'))
jsonlite::write_json(selected, file.path(folder, 'selected_training_games.json'),
                     pretty=TRUE, auto_unbox=TRUE)
cat('Selected',nrow(selected),'training games across',length(unique(selected$patch)),
    'patches. No validation or test outcomes examined.\n')
