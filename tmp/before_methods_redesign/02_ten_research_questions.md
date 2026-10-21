# Ten Research Questions for League of Legends

All ten questions use the same checked ChainCC team dataset: 1,637 available LCK/LEC games dated 2024–2025, paired to one blue-side row per game. R is the analysis tool. Data definitions, common controls, temporal validation, and sources are in `01_data_and_methods.md`. Expected results below are hypotheses, not findings. Q1–Q9 are association or descriptive questions; Q10 is a prediction comparison. Each question has exactly four numbered summary sentences.

## Q1 Does blue side win more often than red side

- **Purpose:** Describe side imbalance in this sample.
- **Data and variables:** One record per game; blue-side `result`, `league`, actual year, and historical team-strength difference for an adjusted comparison.
- **Method and R tools:** Win proportions and week-block bootstrap intervals; logistic regression as an adjusted descriptive check; base R and `ggplot2`.
- **Expected result:** A small blue-side advantage is plausible; a near-even result would also be meaningful.
- **Limitation:** Team strength and side-selection rules can explain an observed difference, so it is not a causal side effect.
- **Keywords:** League of Legends, ChainCC, blue side, win rate, logistic regression, side difference.

**Four sentence summary**

1. I will study whether blue side wins more often than red side in the available LCK and LEC games.
2. I will use side and match outcome from ChainCC, with league and historical team strength as context.
3. I will compare win proportions and use logistic regression in R for an adjusted descriptive check.
4. I expect a small difference, but a near-even result would also help describe side balance in this sample.

## Q2 How is a gold lead at 15 minutes related to winning

- **Purpose:** Estimate the main relationship between early economy and the final result.
- **Data and variables:** Binary blue-side win; `golddiffat15` in 1,000 gold; league and pregame strength difference.
- **Method and R tools:** Logistic regression with a 3-degree-of-freedom natural spline, probability curves, and block-bootstrap intervals; `stats`, `splines`, `ggplot2`.
- **Expected result:** Larger leads should be associated with higher win probabilities; the curve may be nonlinear.
- **Limitation:** Economy reflects earlier play and team strength; this does not measure a causal effect of receiving extra gold.
- **Keywords:** League of Legends, ChainCC, gold lead, 15 minutes, logistic regression, winning.

**Four sentence summary**

1. I will examine how a gold lead at 15 minutes is related to winning.
2. I will use the gold difference, final outcome, league, and historical team strength in the checked ChainCC games.
3. I will fit a logistic regression with a nonlinear gold term in R and plot the predicted win probability.
4. I expect larger leads to be associated with higher winning probabilities, although the relationship may not be linear.

## Q3 Is a kill lead useful after accounting for the gold difference at 15 minutes

- **Purpose:** Separate information in kills from the economy advantage that often comes with them.
- **Data and variables:** Binary win; paired `killdiffat15`, `golddiffat15`, and shared context controls.
- **Method and R tools:** Add kill difference to the gold-and-context logistic model; estimate its conditional association and compare probability scores under the common temporal protocol; base R.
- **Expected result:** Kills may add limited information once gold is included; little gain is a useful finding.
- **Limitation:** Kill and gold differences are correlated, and a conditional association does not prove that securing another kill changes the outcome.
- **Keywords:** League of Legends, ChainCC, kills, gold difference, logistic regression, added information.

**Four sentence summary**

1. I will ask whether a kill lead adds information about winning after accounting for the gold difference at 15 minutes.
2. I will derive the kill difference from both teams' ChainCC records and use the same outcome and context controls.
3. I will add kill difference to the gold-based logistic model in R and examine its conditional association.
4. I expect the added information may be small, which would suggest that gold already captures much of the observed advantage.

## Q4 Does an experience lead add information beyond gold at 15 minutes

- **Purpose:** Assess whether XP provides information beyond measured economy.
- **Data and variables:** Binary win; `xpdiffat15` in 1,000 XP, `golddiffat15`, league and pregame strength.
- **Method and R tools:** Gold-and-context logistic regression with and without XP difference; `stats`, `splines`, and `ggplot2`.
- **Expected result:** XP may retain some association with winning at similar gold differences.
- **Limitation:** Team-total XP does not describe which player has the advantage, and it may be strongly correlated with gold.
- **Keywords:** League of Legends, ChainCC, experience, gold, logistic regression, winning.

**Four sentence summary**

1. I will study whether an experience lead adds information beyond a gold lead at 15 minutes.
2. I will use experience difference, gold difference, match outcome, and shared context variables from ChainCC.
3. I will compare logistic models with and without experience difference in R.
4. I expect experience may add some information, but a weak result would show that its value beyond gold is limited in these games.

## Q5 Does a CS lead add information beyond gold at 15 minutes

- **Purpose:** Examine whether farming-related differences provide information not already summarized by gold.
- **Data and variables:** Binary win; `csdiffat15` in units of 10 CS; gold difference, league, and pregame strength.
- **Method and R tools:** Add CS difference to the gold-and-context logistic model; `stats`, `splines`, and `ggplot2`.
- **Expected result:** The association may be weak after conditioning on gold; it need not have the same sign as the raw association.
- **Limitation:** A CS difference at fixed gold can reflect different ways of earning gold, not simply better farming.
- **Keywords:** League of Legends, ChainCC, creep score, gold difference, logistic regression, conditional association.

**Four sentence summary**

1. I will examine whether a CS lead adds information about winning beyond the gold difference at 15 minutes.
2. I will use CS difference, gold difference, match outcome, and shared context variables in the ChainCC sample.
3. I will fit logistic models in R and compare results before and after adding CS difference.
4. I expect its additional association may be weak, which would help explain how much farming information is already reflected in gold.

## Q6 Does gaining ground from 10 to 15 minutes relate to winning

- **Purpose:** Study changes in the gold advantage after accounting for the starting position.
- **Data and variables:** Binary win; `golddiffat10` and `goldgain10to15 = golddiffat15 - golddiffat10`; shared context.
- **Method and R tools:** Logistic regression with initial gold difference and change, without simultaneously adding the final gold difference; base R and `ggplot2`.
- **Expected result:** A larger increase in advantage should be associated with more wins at a similar 10-minute starting position.
- **Limitation:** Change is not a separate measure of psychological momentum and cannot establish its causal role.
- **Keywords:** League of Legends, ChainCC, gold change, early advantage, logistic regression, winning.

**Four sentence summary**

1. I will study whether gaining ground between 10 and 15 minutes is related to winning.
2. I will calculate the change in gold difference and use the 10-minute difference and context as controls.
3. I will fit a logistic regression in R without adding all three linearly dependent gold terms together.
4. I expect teams that gain ground to win more often at a similar starting position, but this will not prove a causal momentum effect.

## Q7 How often do teams win after trailing by at least 2000 gold at 15 minutes

- **Purpose:** Measure how often a clearly defined early deficit is followed by a comeback.
- **Data and variables:** Games with absolute `golddiffat15 >= 2000`; derived trailing-side win and deficit size; league as descriptive context.
- **Method and R tools:** Comeback proportions, deficit-group summaries, and week-block bootstrap intervals; base R and `ggplot2`.
- **Expected result:** Comebacks should become less common with larger deficits; no exact rate is assumed.
- **Limitation:** The threshold is a project definition, not an official game rule, and subgroup estimates may be imprecise.
- **Keywords:** League of Legends, ChainCC, comeback, gold deficit, proportions, uncertainty.

**Four sentence summary**

1. I will estimate how often a team wins after trailing by at least 2000 gold at 15 minutes.
2. I will identify the trailing team from the ChainCC gold difference and record whether it later wins, once per game.
3. I will calculate comeback proportions and block-bootstrap intervals in R.
4. I expect larger deficits to be followed by fewer comebacks, while the estimated rates will show how much uncertainty remains.

## Q8 Is the gold lead relationship different in LCK and LEC

- **Purpose:** Compare lead conversion across two leagues using comparable gold differences.
- **Data and variables:** Binary win; `golddiffat15`, league, and historical strength difference.
- **Method and R tools:** Logistic regression with a league-by-gold interaction; compare probability curves within overlapping gold ranges; `stats`, `splines`, `ggplot2`.
- **Expected result:** The curves may differ, but no league is assumed to be better at converting leads.
- **Limitation:** League differences combine team strength, selection, scheduling, and format; they do not isolate regional playing style.
- **Keywords:** League of Legends, ChainCC, LCK, LEC, interaction, lead conversion.

**Four sentence summary**

1. I will compare the relationship between the 15-minute gold difference and winning in LCK and LEC.
2. I will use the same gold and outcome measures in both leagues and consider historical team strength.
3. I will fit a league interaction model in R and compare the resulting probability curves.
4. I expect the relationship may differ between leagues, but the analysis will not identify a causal effect of league membership.

## Q9 Does the gold lead relationship change across game patches

- **Purpose:** Explore whether the relationship is stable across versions represented in the data.
- **Data and variables:** Binary win, `golddiffat15`, text-preserved patch, league, and pregame strength.
- **Method and R tools:** Descriptive patch summaries and logistic patch-by-gold interactions for patches with at least 50 games; base R and `ggplot2`.
- **Expected result:** Some variation is plausible; similar relationships would support limited stability across the observed patches.
- **Limitation:** Several patches have small samples, and patches also track time, teams, and tournament formats.
- **Keywords:** League of Legends, ChainCC, game patch, gold lead, interaction, stability.

**Four sentence summary**

1. I will explore whether the relationship between a gold lead and winning changes across game patches.
2. I will use patch codes, gold differences, outcomes, league, and historical team strength from ChainCC.
3. I will compare patch summaries and logistic interactions in R when sample sizes are sufficient.
4. I expect some variation, but it cannot be attributed only to game updates because patches also change with time and competition conditions.

## Q10 Do 15 minute statistics predict outcomes better than 10 minute statistics

- **Purpose:** Quantify the predictive gain from observing five more minutes of play.
- **Data and variables:** Same games and binary outcome for both models; gold, kill, XP, and CS differences at 10 or 15 minutes; identical league and pregame-strength controls.
- **Method and R tools:** Fit matched logistic specifications on 2024 and evaluate on 2025; log loss is primary, with Brier score, AUC, and calibration plots; `stats`, `splines`, `pROC`, `ggplot2`.
- **Expected result:** Fifteen-minute statistics should predict better, but the size and uncertainty of the gain are unknown.
- **Limitation:** Later prediction has less lead time; validation across these two years does not guarantee performance in future seasons.
- **Keywords:** League of Legends, ChainCC, prediction time, logistic regression, temporal validation, log loss.

**Four sentence summary**

1. I will compare how well 10-minute and 15-minute statistics predict the final match outcome.
2. I will use the same ChainCC games and the same types of gold, kill, experience, and CS differences at each time.
3. I will fit models on 2024 games in R and evaluate them on 2025 games using log loss and supporting measures.
4. I expect the later statistics to predict better, but their gain must be considered together with the shorter time left before the result.

## How the questions fit together

Q1 establishes side balance; Q2–Q6 examine early advantages; Q7–Q9 examine comebacks and context; Q10 evaluates prediction over time. All ten appear in the formal proposal. Shared data and models keep the workload manageable without treating ten questions as ten unrelated projects. The longer designs and four-sentence summaries remain here because placing all forty sentences in the one-page proposal would make it unreadable.
