import os
import sys
import cmd
import subprocess

EXPERIMENTAL_TRIAL_FOLDER = "experimentalTrials"
CSV_HEADS = {
    "full1": ",game1plays,game2plays,game3plays,game4plays,game5plays",
    "full2": ",game1plays,game2plays,game3plays,game4plays,game5plays",
    "1": ",letters",
    "2": ",Clubs,Diamonds,Hearts,Spades",
    "3": ",letters",
    "4": ",roll1,roll2",
    "5": ",roll",
}
# PYTHON_LOCATION = "py"

class Wywy(cmd.Cmd):
    intro = "Welcome to Wywy for Frog Jump Testing. Type help to list commands.\n"
    prompt = "Wywy (Frog Jump) >> "
    
    # commands:
    
    def do_play(self, arg):
        "Runs batches of 100,000 trials for entire or individual Frog Jump games (game number -> arg 1) (number of batches? -> arg 2). Only runs if the first arg is OK (arg = full, 1, 2, 3, 4, 5)."
        args = arg.split(" ")
        folderPath = EXPERIMENTAL_TRIAL_FOLDER + "\\"
        scriptPath = EXPERIMENTAL_TRIAL_FOLDER + "\\"
        csvHead = "result"
        # ensure valid input
        match args[0]:
            # case "full" | "fullExperimentalTrials": # alias moment :P
            #     folderPath += "fullExperimentalTrials"
            #     scriptPath += "full.ts"
            case "full1" | "fullExperimentalTrials1":
                folderPath += "fullExperimentalTrials1"
                scriptPath += "fullExperimentalTrials1.ts"
                csvHead += CSV_HEADS["full1"]
            case "full2" | "fullExperimentalTrials2":
                folderPath += "fullExperimentalTrials2"
                scriptPath += "fullExperimentalTrials2.ts"
                csvHead += CSV_HEADS["full2"]
            case "1" | "2" | "3" | "4" | "5":
                folderPath += "game" + args[0]
                scriptPath += "game" + args[0] + "Trials.ts"
                csvHead += CSV_HEADS[args[0]]
            case _:
                print("Wywy smells an invalid input (" + str(args[0]) + ")! Trialtypes can be: full, 1, 2, 3, 4, 5")
                return
        folderPath += "\\"
        
        # make the folder if it doesn't exist
        self.optional_folder_creation(folderPath)

        numDatasets = -1

        if len(args) > 1: # optionally receive an argument via second argument
            try:
                numDatasets = int(args[1])
            except ValueError:
                print("Invalid second argument (needs to be integer). Defaulting to manual user input...\n")

        while numDatasets < 0: # yes, 0 is a valid input because they might not want any datasets. it's a funny yet useless edge case.
            try:
                numDatasets = int(input("How many datasets do you want?: "))
            except ValueError:
                print("Invalid input.\n")
        for i in range(numDatasets):
            if (os.path.isfile(folderPath + "output.csv")):
                # move old the file elsewhere
                f = open(folderPath + "output.csv", "r")
                data = f.read()
                i = 1
                while (os.path.isfile(folderPath + "output" + str(i) + ".csv")):
                    i += 1
                
                f = open(folderPath + "output" + str(i) + ".csv", "w+")
                f.write(data)
                f.close()


            f = open(folderPath + "output.csv", "w+")
            f.write(csvHead)
            f.close()

            process = subprocess.run(["npx", "tsx", scriptPath], shell=True)
    
    def do_bye(self, arg):
        "Exit the Wywy CLI."
        print("Goodbye!")
        self.close()
    
    # helper functions
    def optional_folder_creation(self, path) -> bool:
        """Creates a folder if it doesn't exist

        Args:
            path (str): The path to the folder

        Returns:
            bool: True if a folder should (and has) been created.
        """
        
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return False


        


if __name__ == "__main__":
    Wywy().cmdloop()