# Data adequacy audit. Reads frozen source files; does not fit models.
# Outcomes are summarized only for the initial training subset.
args <- grep('^--file=', commandArgs(FALSE), value=TRUE)
root <- dirname(dirname(normalizePath(sub('^--file=', '', args[[1]]))))
raw_files <- list.files(file.path(root,'data/raw'), pattern='\\.csv\\.gz$', full.names=TRUE)
stopifnot(length(raw_files)==3L)
raw <- do.call(rbind, lapply(raw_files, function(p) read.csv(gzfile(p),
  stringsAsFactors=FALSE, check.names=FALSE, colClasses=c(patch='character'))))
d <- readRDS(file.path(root,'data/derived/eligible_games.rds'))
parts <- readRDS(file.path(root,'audit/proposed_teacher_split_ids.rds'))
stopifnot(!anyDuplicated(d$game_id), nrow(d)==1637L)
b <- raw[raw$side=='Blue',]; r <- raw[raw$side=='Red',]
b <- b[match(d$game_id,b$game_id),]; r <- r[match(d$game_id,r$game_id),]
stopifnot(identical(b$game_id,d$game_id), identical(r$game_id,d$game_id))
features <- c('golddiffat15','killdiffat15','xpdiffat15','csdiffat15')
required <- c('game_id','date','league','patch','team_id','red_team_id','result',features)
checks <- c(
  raw_duplicate_game_side_keys=sum(duplicated(paste(raw$game_id,raw$side))),
  raw_games_without_two_rows=sum(table(raw$game_id)!=2L),
  missing_required_cells=sum(is.na(d[required]) | d[required]==''),
  nonbinary_results=sum(!d$result %in% c(TRUE,FALSE)),
  noncomplementary_paired_results=sum(as.integer(b$result)+as.integer(r$result)!=1L),
  nonpositive_gold15=sum(b$goldat15<=0 | r$goldat15<=0),
  no_15minute_snapshot_duration=sum(b$gamelength<=900 | r$gamelength<=900),
  inconsistent_gold_difference=sum(abs((b$goldat15-r$goldat15)-b$golddiffat15)>1),
  inconsistent_paired_context=sum(b$date!=r$date | b$league!=r$league | b$patch!=r$patch),
  same_team_on_both_sides=sum(b$team_id==r$team_id),
  kills_exceed_opposing_deaths=sum(b$killsat15>r$deathsat15 | r$killsat15>b$deathsat15),
  repeated_natural_match_keys=sum(duplicated(paste(d$league,d$date,
    pmin(d$team_id,d$red_team_id),pmax(d$team_id,d$red_team_id),d$game_number))),
  derived_gold_mismatches=sum(d$golddiffat15!=b$golddiffat15),
  derived_kill_mismatches=sum(d$killdiffat15!=b$killsat15-r$killsat15),
  derived_experience_mismatches=sum(d$xpdiffat15!=b$xpdiffat15),
  derived_creep_mismatches=sum(d$csdiffat15!=b$csdiffat15)
)
for (v in c('golddiffat15','xpdiffat15','csdiffat15')) {
  checks[paste0('nonopposite_',v)] <- sum(abs(b[[v]]+r[[v]])>1)
}
finite <- vapply(d[features],function(z) sum(!is.finite(z)),integer(1))
stopifnot(all(checks==0), all(finite==0))
train <- d[d$game_id %in% parts$train_korea_2024_jan_jun,]
validation <- d[d$game_id %in% parts$validation_korea_2024_jul_sep,]
source <- rbind(train,validation)
stopifnot(nrow(train)==313L,nrow(validation)==169L,nrow(source)==482L)
summaries <- do.call(rbind,lapply(names(parts),function(n){
  z <- d[match(parts[[n]],d$game_id),]
  data.frame(part=n,games=nrow(z),teams=length(unique(c(z$team_id,z$red_team_id))),
    patches=length(unique(z$patch)),weeks=length(unique(cut(as.Date(substr(z$date,1,10)),
      'weeks',start.on.monday=TRUE))),missing_features=sum(is.na(z[features])),
    constant_features=sum(vapply(z[features],function(x) length(unique(x))<=1,logical(1))))
}))
training_feature_summary <- data.frame(field=features,
  min=vapply(train[features],min,numeric(1)),max=vapply(train[features],max,numeric(1)),
  sd=vapply(train[features],sd,numeric(1)),
  distinct=vapply(train[features],function(x)length(unique(x)),integer(1)),row.names=NULL)
X <- cbind(Intercept=1,scale(train[features]))
training_design_rank <- qr(X)$rank
source_patch_counts <- table(source$patch)
source_patch_support <- do.call(rbind,lapply(names(source_patch_counts),function(p){
  z <- source[source$patch==p,]
  data.frame(patch=p,games=nrow(z),gold_distinct=length(unique(z$golddiffat15)),
             gold_negative=sum(z$golddiffat15<0),gold_positive=sum(z$golddiffat15>0))
}))
class_counts <- table(factor(train$result,levels=c(FALSE,TRUE),labels=c('blue_loss','blue_win')))
ratio <- min(class_counts)/ncol(X)
all_part_ids <- unlist(parts,use.names=FALSE)
stopifnot(!anyDuplicated(all_part_ids),setequal(all_part_ids,d$game_id))
lines <- c('# Data readiness audit', '',
  'Audit date: 2026-10-20. No models fitted. Validation and test outcomes were not summarized or associated with predictors.', '',
  '## Frozen source and derived-data consistency', capture.output(print(checks)),
  'Nonfinite feature values:',capture.output(print(finite)), '',
  '## Partition support',capture.output(print(summaries,row.names=FALSE)), '',
  'The final source refit is training plus validation (482 games), not an extra independent partition.',
  'All partitions are disjoint and together match the saved cohort.', '',
  '## Initial training subset only',
  'Outcome counts:',capture.output(print(class_counts)),
  'Predictor ranges and variation:',capture.output(print(training_feature_summary,row.names=FALSE)),
  paste('Linear design rank including intercept:',training_design_rank,'of',ncol(X)),
  paste('Standardized design condition number:',format(kappa(X,exact=TRUE),digits=5)),
  paste('Smaller class count per linear-model coefficient including intercept:',format(ratio,digits=4)),
  'This ratio is a descriptive workload check, not a sample-size sufficiency theorem or power calculation.',
  'Training predictor correlation:',capture.output(print(round(cor(train[features]),3))), '',
  '## Source refit patch support (no outcome grouping)',
  capture.output(print(source_patch_support,row.names=FALSE)),
  paste('Patch groups:',length(source_patch_counts)),
  paste('Patch count range:',min(source_patch_counts),'to',max(source_patch_counts)),
  'Random-slope precision and between-patch variance remain uncertain with this number of groups.', '',
  '## Independent verification boundary',
  'Internal agreement does not independently establish correct timestamps, definitions, completeness, or event measurement.',
  'No test scores, test win rates, or predictor-outcome associations were computed for this audit.')
writeLines(lines,file.path(root,'audit/data_readiness_2026-10-20.md'))
saveRDS(list(checks=checks,partitions=summaries,training_class_counts=class_counts,
  training_features=training_feature_summary,training_rank=training_design_rank,
  training_condition_number=kappa(X,exact=TRUE),source_patch_support=source_patch_support),
  file.path(root,'audit/data_readiness_2026-10-20.rds'))
cat(paste(lines,collapse='\n'),'\n')
