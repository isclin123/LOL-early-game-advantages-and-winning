# Counts and field checks for a proposed split; no models or outcome summaries.
args <- grep('^--file=', commandArgs(FALSE), value = TRUE)
root <- dirname(dirname(normalizePath(sub('^--file=', '', args[[1]]))))
d <- readRDS(file.path(root, 'data/derived/eligible_games.rds'))
day <- as.Date(substr(d$date, 1, 10))
parts <- list(
  train_korea_2024_jan_jun = which(d$league == 'LCK' & day >= as.Date('2024-01-01') & day < as.Date('2024-07-01')),
  validation_korea_2024_jul_sep = which(d$league == 'LCK' & day >= as.Date('2024-07-01') & day < as.Date('2024-10-01')),
  test_temporal_korea_2025 = which(d$league == 'LCK' & format(day, '%Y') == '2025'),
  test_external_europe_2025 = which(d$league == 'LEC' & format(day, '%Y') == '2025'),
  unused_europe_2024 = which(d$league == 'LEC' & format(day, '%Y') == '2024')
)
ids <- unlist(parts, use.names=FALSE)
stopifnot(length(ids) == nrow(d), !anyDuplicated(ids), !anyDuplicated(d$game_id),
          identical(as.integer(lengths(parts)), c(313L,169L,555L,306L,294L)))
required <- c('golddiffat15', 'killdiffat15', 'xpdiffat15', 'csdiffat15', 'patch',
              'team_id', 'red_team_id', 'date', 'league', 'result')
stopifnot(all(required %in% names(d)), !anyNA(d[required]))
summary <- do.call(rbind, lapply(names(parts), function(n) {
  z <- d[parts[[n]], ]; dz <- day[parts[[n]]]
  data.frame(part=n, games=nrow(z), first_date=as.character(min(dz)),
             last_date=as.character(max(dz)), patches=length(unique(z$patch)),
             weeks=length(unique(cut(dz, 'weeks', start.on.monday=TRUE))))
}))
source_rows <- c(parts[[1]], parts[[2]])
patch_counts <- table(d$patch[source_rows])
source_patches <- unique(d$patch[source_rows])
lines <- c('# Teacher revision data feasibility', '',
           'Planned split only. No win proportions, fitted models, or predictive scores were computed.', '',
           capture.output(print(summary, row.names=FALSE)), '',
           paste('Source-league final refit games:', length(source_rows)),
           paste('Source-league patch groups:', length(patch_counts)),
           paste('Source-league games per patch:', min(patch_counts), 'to', max(patch_counts)),
           paste('2025 test patch codes overlapping source 2024:',
                 length(intersect(source_patches, unique(d$patch[c(parts[[3]],parts[[4]])])))),
           'All proposed partitions are disjoint and together account for the saved 1,637-game cohort.',
           'All required fields exist and are nonmissing; this does not independently validate their measurement.',
           'The test patch codes are new to the source fit. Bayesian forecasts must integrate over new group effects.')
writeLines(lines, file.path(root, 'audit/teacher_revision_feasibility.md'))
saveRDS(lapply(parts, function(ix) d$game_id[ix]), file.path(root,'audit/proposed_teacher_split_ids.rds'))
cat(paste(lines, collapse='\n'), '\n')
