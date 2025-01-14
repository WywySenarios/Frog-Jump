# import libraries
library(showtext)

# font stuff
font_add_google("Quicksand", "quicksand")

# enable showtext for font rendering
showtext_auto()

par(family = "quicksand")



# the number of raw trials that are run to gain a single datapoint.
trialSize <- 100000

# full experimental trials where the frog starts at lily pad #1
fullExperimentalTrials1 <- read.csv("data/computerizedData/fullExperimentalTrials1.csv")
fullExperimentalTrials2 <- read.csv("data/computerizedData/fullExperimentalTrials2.csv")

# trials for the single game only
game1 <- read.csv("data/computerizedData/game1.csv")
game2 <- read.csv("data/computerizedData/game2.csv")
game3 <- read.csv("data/computerizedData/game3.csv")
game4 <- read.csv("data/computerizedData/game4.csv")
game5 <- read.csv("data/computerizedData/game5.csv")

# what do you want to plot a histogram of?
singleVarStatsTitles <- list("Winrate When Starting From Lily Pad 1",
                             "Winrate When Starting From Lily Pad 2",
                             "Minigame 1 Winrate",
                             "Minigame 2 Winrate",
                             "Minigame 3 Winrate",
                             "Minigame 4 Winrate",
                             "Minigame 5 Winrate",
                             )
singleVarStats <- list(fullExperimentalTrials1$W,
                       game1,
                       game2,
                       game3,
                       game4,
                       game5,)


findWinProbability <- function(point) point / trialSize

for (x in 1:length(singleVarStats)) {
  hist(unlist(lapply(singleVarStats[x], findWinProbability)),
       main=singleVarStatsTitles[x],
       xlab="Winrate",
       col="#4285f4",
       include.lowest = TRUE,
       )
}