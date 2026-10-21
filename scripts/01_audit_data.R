# Structural feasibility audit only. No hypothesis tests or predictive models.
args <- grep('^--file=', commandArgs(FALSE), value = TRUE)
script <- if (length(args)) sub('^--file=', '', args[[1]]) else sys.frame(1)$ofile
root <- dirname(dirname(normalizePath(script, mustWork = TRUE)))
setwd(root)
dir.create('audit', showWarnings = FALSE)
files <- list.files('data/raw', pattern = '\\.csv\\.gz$', full.names = TRUE)
stopifnot(length(files) == 3L)
frames <- lapply(files, function(f) {
  x <- read.csv(gzfile(f), stringsAsFactors = FALSE, check.names = FALSE,
                colClasses = c(patch='character'))
  x$source_file <- basename(f)
  x
})
all <- do.call(rbind, frames)
needed <- c('game_id','date','league','patch','side','team_id','opponent_team_name',
            'result','gamelength','goldat10','golddiffat10','xpdiffat10','csdiffat10',
            'goldat15','golddiffat15','xpdiffat15','csdiffat15','killsat15','deathsat15')
stopifnot(all(needed %in% names(all)))
lines <- c('# LOL source feasibility audit', '',
           paste('Checked UTC:', format(Sys.time(), tz='UTC', usetz=TRUE)),
           'No model was fitted and no outcome associations were calculated.', '')
for (i in seq_along(frames)) {
  x <- frames[[i]]
  lines <- c(lines, paste('##', basename(files[i])),
    paste('Rows:', nrow(x), '; columns excluding source label:', ncol(x)-1L),
    paste('Unique game IDs:', length(unique(x$game_id))),
    paste('Date range:', min(x$date, na.rm=TRUE), 'to', max(x$date, na.rm=TRUE)),
    'Date year counts:', capture.output(table(substr(x$date,1,4), useNA='ifany')),
    'League counts:', capture.output(sort(table(x$league),decreasing=TRUE)),
    'Missing values in required fields:', capture.output(colSums(is.na(x[needed]) | x[needed]=='')), '')
}
keys <- paste(all$game_id, all$side, sep='|')
lines <- c(lines,'## Cross-file checks', paste('Repeated game-side keys:',sum(duplicated(keys))),
           'Rows per game:',capture.output(table(table(all$game_id))),
           'Side codes:',capture.output(table(all$side)),
           'Result codes:',capture.output(table(all$result,useNA='ifany')))
cohort <- all[substr(all$date,1,4) %in% c('2024','2025') & all$league %in% c('LCK','LPL','LEC'), ]
lines <- c(lines,'','## Candidate actual-date cohort: LCK LPL LEC in 2024 and 2025',
           paste('Team rows:',nrow(cohort)),paste('Unique games:',length(unique(cohort$game_id))),
           capture.output(table(cohort$league,substr(cohort$date,1,4))),
           'Required-field missingness:',capture.output(colSums(is.na(cohort[needed]) | cohort[needed]=='')),
           'Patch counts:',capture.output(table(cohort$patch)))
blue <- cohort[cohort$side=='Blue',]
red <- cohort[cohort$side=='Red',]
red <- red[match(blue$game_id,red$game_id),]
stopifnot(all(blue$game_id==red$game_id))
numeric_fields <- c('gamelength','goldat10','goldat15','golddiffat10','golddiffat15',
                    'xpdiffat15','csdiffat15','killsat15','deathsat15')
bad_outcome <- as.integer(blue$result)+as.integer(red$result)!=1L
bad_early <- blue$goldat10<=0 | red$goldat10<=0 | blue$goldat15<=0 | red$goldat15<=0
early_end <- blue$gamelength<=900 | red$gamelength<=900
diff_fields <- c('golddiffat10','golddiffat15','xpdiffat10','xpdiffat15','csdiffat10','csdiffat15')
bad_diff <- Reduce(`|`,lapply(diff_fields,function(v) abs(blue[[v]]+red[[v]])>1))
bad_gold <- abs((blue$goldat15-red$goldat15)-blue$golddiffat15)>1 | abs((blue$goldat10-red$goldat10)-blue$golddiffat10)>1
# Deaths may exceed opposing kills because an execution need not credit a player.
# Report this diagnostic but do not delete such valid matches.
kill_death_difference <- blue$killsat15!=red$deathsat15 | red$killsat15!=blue$deathsat15
bad_kills <- blue$killsat15>red$deathsat15 | red$killsat15>blue$deathsat15
bad_context <- blue$date!=red$date | blue$league!=red$league | blue$patch!=red$patch | blue$gamelength!=red$gamelength
eligible <- !(bad_outcome | bad_early | early_end | bad_diff | bad_gold | bad_kills | bad_context)
lines <- c(lines,'','## Paired game validation',
  paste('Noncomplementary results:',sum(bad_outcome)),paste('Zero or negative early total gold:',sum(bad_early)),
  paste('Games ending at or before 15 minutes:',sum(early_end)),
  paste('Nonopposite recorded differences:',sum(bad_diff)),paste('Gold totals inconsistent with differences:',sum(bad_gold)),
  paste('Any kill/death difference at 15 (not an exclusion):',sum(kill_death_difference)),
  paste('Opposing kills exceed recorded deaths:',sum(bad_kills)),paste('Cross-side context mismatch:',sum(bad_context)),
  'Nonpositive early gold by league:',capture.output(table(blue$league,bad_early)),
  paste('Eligible paired games:',sum(eligible)),
  'Eligible games by actual year and league:',capture.output(table(blue$league[eligible],substr(blue$date[eligible],1,4))),
  'Numeric ranges:',capture.output(sapply(blue[numeric_fields],range,na.rm=TRUE)))
dir.create('data/derived',showWarnings=FALSE)
blue$red_team_id <- red$team_id
blue$red_team_name <- red$team_name
blue$killdiffat15 <- blue$killsat15-red$killsat15
blue$killdiffat10 <- blue$killsat10-red$killsat10
blue$goldgain10to15 <- blue$golddiffat15-blue$golddiffat10
saveRDS(blue[eligible,], 'data/derived/eligible_games.rds')
summary <- list(source_team_rows=nrow(all),candidate_games=nrow(blue),eligible_games=sum(eligible),
                years=table(substr(blue$date[eligible],1,4)),leagues=table(blue$league[eligible]))
dput(summary,'audit/cohort_summary.R')
writeLines(lines,'audit/data_audit.md',useBytes=TRUE)
cat(paste(lines,collapse='\n'),'\n')
