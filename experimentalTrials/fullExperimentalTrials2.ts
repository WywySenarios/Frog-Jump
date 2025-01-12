import fs from "fs";
// START: File storage
const filePath = "experimentalTrials\\fullExperimentalTrials2\\";
/**
 * Output in the form of W or L, proceeded by an integer number of games played, in a object like form.
 * {game1, game2, etc.}
 * e.g. W{0,1,1,1,1}L{1,0,0,0,0}
 */
let output: fs.WriteStream = fs.createWriteStream(filePath + "output.csv", {
   flags: "a",
});

/**
 * Log the events that have happened.
 */
// let log: fs.WriteStream = fs.createWriteStream(filePath + "log.txt", {
//    flags: "a", // append the content to the file
// });
// log.write("LOG BEGIN: " + (new Date(Date.now())).toString() + "\n");
// END: File storage

// START: config
const startingLilyPad = 2;
const numTrials = 100000;
// const numTrials = 100;
// END: config

/**
 * Defines the game status.
 * This should contain the following information:
 * * which lily pad the player is currently on.
 * * the bet the player initially made (lily pad number).
 * * Whether or not a minigame is currently being played
 */
let gameStatus = {
   pad: 0,
   bet: -1,
   nextGame: placeholder,
   nextPressed: true,
};
let gameData = {
   0: null,
   1: {
      letters: ["F", "A", "T", "E"],
   },
   2: {
   },
   3: {
      letters: ["P", "R", "O", "B", "A", "B", "I", "L", "I", "T", "Y"],
   },
};
const defaultGameStatus = {
   pad: 0,
   bet: -1,
   nextGame: placeholder,
   nextPressed: true,
};
/**
 * This contains all the game functions, which process game logic.
 */
let gameFunctions = {
   0: placeholder,
   1: firstLilyPad,
   2: secondLilyPad,
   3: thirdLilyPad,
   4: fourthLilyPad,
   5: fifthLilyPad,
   6: placeholder,
};

type Card = {
   suit: string;
};
// END Deck related variables

/**
 * Contains information relating to all cards. Links their numerical ID to a file path and whatnot.
 */
const cardData: Record<number, Card> = {
   1: {
      suit: "Clubs",
   },
   2: {
      suit: "Clubs",
   },
   3: {
      suit: "Clubs",
   },
   4: {
      suit: "Clubs",

   },
   5: {
      suit: "Clubs",

   },
   6: {
      suit: "Clubs",

   },
   7: {
      suit: "Clubs",

   },
   8: {
      suit: "Clubs",

   },
   9: {
      suit: "Clubs",

   },
   10: {
      suit: "Clubs",

   },
   11: {
      suit: "Clubs",

   },
   12: {
      suit: "Clubs",

   },
   13: {
      suit: "Clubs",

   },
   14: {
      suit: "Diamond",

   },
   15: {
      suit: "Diamond",

   },
   16: {
      suit: "Diamond",

   },
   17: {
      suit: "Diamond",

   },
   18: {
      suit: "Diamond",

   },
   19: {
      suit: "Diamond",

   },
   20: {
      suit: "Diamond",

   },
   21: {
      suit: "Diamond",

   },
   22: {
      suit: "Diamond",

   },
   23: {
      suit: "Diamond",

   },
   24: {
      suit: "Diamond",

   },
   25: {
      suit: "Diamond",

   },
   26: {
      suit: "Diamond",

   },
   27: {
      suit: "Hearts",

   },
   28: {
      suit: "Hearts",

   },
   29: {
      suit: "Hearts",

   },
   30: {
      suit: "Hearts",

   },
   31: {
      suit: "Hearts",

   },
   32: {
      suit: "Hearts",

   },
   33: {
      suit: "Hearts",

   },
   34: {
      suit: "Hearts",

   },
   35: {
      suit: "Hearts",

   },
   36: {
      suit: "Hearts",

   },
   37: {
      suit: "Hearts",

   },
   38: {
      suit: "Hearts",

   },
   39: {
      suit: "Hearts",

   },
   40: {
      suit: "Spades",

   },
   41: {
      suit: "Spades",

   },
   42: {
      suit: "Spades",

   },
   43: {
      suit: "Spades",

   },
   44: {
      suit: "Spades",

   },
   45: {
      suit: "Spades",

   },
   46: {
      suit: "Spades",

   },
   47: {
      suit: "Spades",

   },
   48: {
      suit: "Spades",

   },
   49: {
      suit: "Spades",

   },
   50: {
      suit: "Spades",

   },
   51: {
      suit: "Spades",

   },
   52: {
      suit: "Spades",

   },
};
function onBetButtonClick() {
   gameStatus = {
      pad: startingLilyPad,
      bet: startingLilyPad,
      nextGame: gameFunctions[startingLilyPad],
      nextPressed: true,
   };

   // log.write("Bet: " + startingLilyPad + "\n");
}

function postGame(): void {
   // reset game
   gameStatus = defaultGameStatus;

   gameStatus.nextPressed = false; // let the onBetButtonClicked function know that they need to reset the game area.
}

/**
 * 
 * @returns -1 if the gameStatus is invalid
 * @returns 0 if the game has not been won or lost
 * @returns 1 if the game has been lost
 * @returns 2 if the game has been won.
 * @returns false if there is something wrong with the game state.
 */
function playNextGame(): number {
   switch (gameStatus.pad) {
      case 0: // the game hasn't started yet
         return -1;
      case 1:
         break;
      case 2:
         break;
      case 3:
         break;
      case 4:
         break;
      case 5:
         break;
      default:
         return -1;
   }


   let win = gameStatus.nextGame();

   // win/loss logic
   if (win === true) {
      // win
      gameStatus.pad++;

      // if the player has successfully won the game,
      if (gameStatus.pad == 6) {
         postGame();
         return 2; // avoid new game functions being set
      }
   } else if (win === false) {
      // loss
      gameStatus.pad--;

      // COMPLETE loss; the frog has been eaten by the snake
      if (gameStatus.pad == 0) {
         postGame();
         return 1; // avoid new game functions being set
      }
   } else {
   }

   //@ts-ignore
   gameStatus.nextGame = gameFunctions[gameStatus.pad];

   return 0;
}

function placeholder(): any {
   const message = "PENDING BET. PLEASE CLICK ON BET.";
   console.log("A placeholder function has been called.");
   // if (gameStatusElement != null) {
   //    gameStatusElement.innerHTML = "PENDING BET. PLEASE CLICK ON BET.";
   // }

   return;
}

// MINIGAME LOGIC
/**
 * Plays the game and animations for a lily pad's game.
 * Returns the next function of the next lily pad OR returns a placeholder function and immediately executes win/loss code.
 */
function firstLilyPad() {
   numGamesPlayed[1]++;
   // game logic
   let gameResult = ["F", "A", "T", "E"]; // pass in by REFERENCE
   shuffleLetters(gameResult);

   // if the index of the A is smaller than the E,
   // that means that the A is before the E,
   // which means that the player loses.
   if (
      gameResult.findIndex((element) => element == "A") <
      gameResult.findIndex((element) => element == "E")
   ) {
      // loss
      return false;
   } else {
      // win
      return true;
   }
}

function secondLilyPad() {
   numGamesPlayed[2]++;
   // game logic
   // pick, at random, 4 cards from the deck.
   let deck: Array<number> = [];
   for (let i = 0; i < 52; i++) {
      deck[i] = i + 1;
   }

   // shuffle deck
   for (let i = deck.length - 1; i >= 0; i--) {
      let j = Math.floor(Math.random() * (i + 1));

      let temp = deck[i];
      deck[i] = deck[j];
      deck[j] = temp;
   }

   // take top 4 cards from deck
   const pickedCards: Array<number> = [deck[0], deck[1], deck[2], deck[3]];

   // count the number of cards in each suit
   let numberOfSuits = {
      Clubs: 0,
      Diamond: 0,
      Hearts: 0,
      Spades: 0,
   };
   for (let i of pickedCards) {
      // HOPEFULLY DOES NOT CAUSE ERRORS, just make sure the deck constant is OK
      numberOfSuits[cardData[i].suit]++;
   }

   // if all the cards are in different suits,
   if (
      numberOfSuits["Clubs"] == 1 &&
      numberOfSuits["Diamond"] == 1 &&
      numberOfSuits["Hearts"] == 1 &&
      numberOfSuits["Spades"] == 1
   ) {
      // loss
      return false;
   } else if (
      (function winCondition() {
         // remember that exactly TWO cards have to be in the same suit in order to win.
         // This means that having 3 cards in the same suit will result in a tie, and having 2 cards as the same suit but 2 cards in another suit will also result in a tie.
         let numTwoCards: number = 0;
         //@ts-ignore numberOfSuits ONLY has strings as keys, as defined earlier.
         for (let i in numberOfSuits) {
            //@ts-ignore
            if (numberOfSuits[i] == 2) numTwoCards++;
         }
         return numTwoCards == 1;
      })()
   ) {
      // win
      return true;
   }
}

function thirdLilyPad() {
   numGamesPlayed[3]++;
   // game logic
   let gameResult = ["P", "R", "O", "B", "A", "B", "I", "L", "I", "T", "Y"];
   shuffleLetters(gameResult);

   // if two letters are one index away from each other,
   // they must be touching.
   // The player loses if two letters are touching.
   let Bs = [gameResult.indexOf("B")];
   Bs.push(gameResult.indexOf("B", Bs[0] + 1)); // this will NEVER error given that there are two B's in PROBABILITY
   let Is = [gameResult.indexOf("I")];
   Is.push(gameResult.indexOf("I", Is[0] + 1));
   if (Math.abs(Bs[0] - Bs[1]) == 1 || Math.abs(Is[0] - Is[1]) == 1) {
      // loss
      return false;
   } else {
      // win
      return true;
   }
}

function fourthLilyPad() {
   numGamesPlayed[4]++;
   let gameResult = [Math.floor(Math.random() * 6 + 1), Math.floor(Math.random() * 6 + 1)];
   // if one die is a multiple of the other,
   // AKA if the first die is a multiple of the second die OR the second die is a multiple of the first die,
   if (
      gameResult[0] % gameResult[1] == 0 ||
      gameResult[1] % gameResult[0] == 0
   ) {
      return false;
   } else {
      // the win condition is to not lose! :D
      return true;
   }
}

function fifthLilyPad() {
   numGamesPlayed[5]++;

   let rollNumber = Math.floor(Math.random() * 7 + 1);
   // if (rollNumber == 7) {
   //    rollNumber = 1;
   // } // avoid this edge case. IDK what's up with JS nowadays.

   // you win if you land on region 1 or 4, starting from vertical position (N),
   switch (rollNumber) {
      case 1: // curse javascript stupid syntax! XD
      case 4:
         return true;
      default:
         return false;
   }
}
// END: MINIGAME LOGIC

/**
 * Shuffles letters and returns the final result.
 * NOTE: passing in the array by reference makes it so that you don't have to store the return value of this function.
 * @param letters: An array with pairs of letters and nodes.
 * Coded with logic pulled from https://dev.to/codebubb/how-to-shuffle-an-array-in-javascript-2ikj
 */
function shuffleLetters(letters: Array<String>) {
   for (let i = letters.length - 1; i >= 0; i--) {
      let j = Math.floor(Math.random() * (i + 1));

      // Swap values at i and j, the randomly generated location.
      let temp = letters[i];
      letters[i] = letters[j];
      letters[j] = temp;
   }

   // console.log("Done shuffling letters: ", letters);
   return letters;
}
// END: DICE ROLL LOGIC



// Recorder logic

let numGamesPlayed = {
   1: 0,
   2: 0,
   3: 0,
   4: 0,
   5: 0,
};
let numGames = 0;

let lastGame: number;

while (numGames < numTrials) {
   // setup the game
   onBetButtonClick();
   lastGame = 0;
   numGamesPlayed = {
      1: 0,
      2: 0,
      3: 0,
      4: 0,
      5: 0,
   };

   while (lastGame == 0) {
      lastGame = playNextGame();
   }

   if (lastGame == 1) { // loss
      output.write("\nL");
      // console.log("\nL" + JSON.stringify(numGamesPlayed));
   } else if (lastGame == 2) { // win
      output.write("\nW");
      // console.log("W" + JSON.stringify(numGamesPlayed));
   } else {
      console.log("Last game has an invalid value???: ", lastGame);
   }

   for (let i in numGamesPlayed) {
      output.write("," + numGamesPlayed[i])
   }

   numGames++;
}

output.end()
// log.end()