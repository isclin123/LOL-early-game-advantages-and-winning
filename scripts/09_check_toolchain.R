# Toolchain readiness check for analysis steps 3-5. Confirms the modelling
# packages named in 04_analysis_plan.md are installed and that a Stan model of
# the planned shape compiles and samples here. Simulated data only: reads no
# project data and produces no analysis results. Takes about 7-8 minutes,
# nearly all of it Stan compilation.
args <- grep('^--file=', commandArgs(FALSE), value=TRUE)
root <- dirname(dirname(normalizePath(sub('^--file=', '', args[[1]]))))
stopifnot(dir.exists(file.path(root,'audit')))
features <- c('gold15_z','kills15_z','experience15_z','creep15_z')

required <- c('brms','rstan','StanHeaders','ranger','randomForest','loo',
  'bayesplot','posterior','cluster','pROC','lme4')
stopifnot(all(vapply(required, requireNamespace, logical(1), quietly=TRUE)))
versions <- vapply(required, function(p) as.character(packageVersion(p)), character(1))
build_tools <- pkgbuild::has_build_tools(debug=FALSE)
stopifnot(isTRUE(build_tools))
# brms reserves the 'sp_' and 'cs_' name prefixes; creep15_z is unaffected.
prefix_clash <- any(grepl('^(sp_|cs_)', features))
stopifnot(!prefix_clash)

set.seed(1)
n <- 300L
sim <- data.frame(patch=sample(paste0('14.',1:8), n, TRUE), gold15_z=rnorm(n),
  kills15_z=rnorm(n), experience15_z=rnorm(n), creep15_z=rnorm(n))
sim$y <- rbinom(n, 1, plogis(0.1 + 1.2*sim$gold15_z + 0.3*sim$kills15_z))

suppressMessages(library(ranger))
forest <- ranger(factor(y) ~ ., data=sim[c('y',features)], probability=TRUE,
  num.trees=500, mtry=2, min.node.size=10, seed=42)
forest_probs <- predict(forest, sim[features])$predictions[,'1']
stopifnot(all(forest_probs >= 0), all(forest_probs <= 1))

suppressMessages(library(brms))
started <- Sys.time()
fit <- brm(y ~ gold15_z + kills15_z + experience15_z + creep15_z +
    (1 + gold15_z || patch), data=sim, family=bernoulli(),
  prior=c(prior(normal(0,1), class='b'), prior(normal(0,1.5), class='Intercept'),
    prior(exponential(1), class='sd')),
  chains=2, iter=600, warmup=300, seed=42, refresh=0, backend='rstan')
elapsed <- as.numeric(difftime(Sys.time(), started, units='secs'))
divergences <- sum(vapply(rstan::get_sampler_params(fit$fit, inc_warmup=FALSE),
  function(z) sum(z[,'divergent__']), numeric(1)))

# Every 2025 test patch is new, so step 5 depends on new-level prediction.
unseen <- data.frame(patch='15.99', gold15_z=c(-1,0,1), kills15_z=0,
  experience15_z=0, creep15_z=0)
epred <- posterior_epred(fit, newdata=unseen, allow_new_levels=TRUE,
  sample_new_levels='gaussian')
unseen_means <- colMeans(epred)
stopifnot(dim(epred)==c(600L,3L), all(unseen_means > 0), all(unseen_means < 1))

result <- list(check_date='2026-10-20', r_version=R.version.string,
  stan_build_tools_available=build_tools, packages=as.list(versions),
  brms_reserved_prefix_clash=prefix_clash, ranger_probability_forest_ok=TRUE,
  planned_formula_compiled=TRUE, compile_and_sample_seconds=round(elapsed),
  max_rhat=round(max(brms::rhat(fit), na.rm=TRUE), 4),
  divergent_transitions=divergences, unseen_level_prediction_ok=TRUE,
  unseen_patch_mean_probabilities=round(unname(unseen_means), 3),
  fitted_on='simulated data only', project_data_read=FALSE,
  analysis_results_produced=FALSE)
jsonlite::write_json(result, file.path(root,'audit/toolchain_check_2026-10-20.json'),
  pretty=TRUE, auto_unbox=TRUE)
cat('Toolchain check passed in', round(elapsed), 'seconds.\n')
