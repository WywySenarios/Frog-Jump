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
fullExperimentalTrials3 <- read.csv("data/computerizedData/fullExperimentalTrials3.csv")

# trials for the single game only
game1 <- read.csv("data/computerizedData/game1.csv")
game2 <- read.csv("data/computerizedData/game2.csv")
game3 <- read.csv("data/computerizedData/game3.csv")
game4 <- read.csv("data/computerizedData/game4.csv")
game5 <- read.csv("data/computerizedData/game5.csv")

# what do you want to plot a histogram of?
titles <- list(
  "Winrate When Starting From Lily Pad 1",
  "Winrate When Starting From Lily Pad 3",
  "Minigame 1 Winrate",
  "Minigame 2 Winrate",
  "Minigame 3 Winrate",
  "Minigame 4 Winrate",
  "Minigame 5 Winrate"
)
wins <- list(
  fullExperimentalTrials1$W,
  fullExperimentalTrials3$W,
  game1$W,
  game2$W,
  game3$W,
  game4$W,
  game5$W
)
losses <- list(
  fullExperimentalTrials1$L,
  fullExperimentalTrials3$L,
  game1$L,
  game2$L,
  game3$L,
  game4$L,
  game5$L
)
colors <- c(
  "#4285f4",
  "#4285f4",
  "#4285f4",
  "#DB4437",
  "#F4B400",
  "#0F9D58",
  "#ff6d01"
)

findWinProbability <- function(point) point / trialSize

for (x in 1:length(wins)) {
  hist(unlist(lapply(wins[x], findWinProbability)),
  #hist(unlist(wins[x]),
    freq = FALSE,
    main = titles[x],
    #xlab = "Wins (/100 000)",
    xlab = "Winrate",
    col = colors[x],
  )
  box()

  thisWins <- sum(unlist(wins[x]))
  thisLosses <- sum(unlist(losses[x]))

  print(paste("P(", titles[x], ") = ", str((thisWins) / (thisWins + thisLosses)), sep="" ))
  print(paste("Total Wins(", thisWins, "): ", sep=""))
  print(paste("Total Losses(", thisLosses, "): ", sep=""))
}
