import os
import csv
import cmd
import subprocess
import shutil

EXPERIMENTAL_TRIAL_FOLDER = "experimentalTrials"
CSV_HEADS = {
    "full1": "result,game1plays,game2plays,game3plays,game4plays,game5plays",
    "full2": "result,game1plays,game2plays,game3plays,game4plays,game5plays",
    "full3": "result,game1plays,game2plays,game3plays,game4plays,game5plays",
    "1": "result,letters",
    "2": "result,Clubs,Diamonds,Hearts,Spades",
    "3": "result,letters",
    "4": "result,roll1,roll2",
    "5": "result,roll",
}
DECIMATION_METHODS = {
    "fullExperimentalTrials1": [["count", "W", "L"], ["sum"], ["sum"], ["sum"], ["sum"], ["sum"]],
    "fullExperimentalTrials2": [["count", "W", "L"], ["sum"], ["sum"], ["sum"], ["sum"], ["sum"]],
    "fullExperimentalTrials3": [["count", "W", "L"], ["sum"], ["sum"], ["sum"], ["sum"], ["sum"]],
    "game1": [["count", "W", "L"], ["count", "EFTA", "EFAT", "ETAF", "ETFA", "EFA", "FAET", "FATE", "FEAT", "FETA", "FTAE", "FTEA", "ATEF", "ATFE", "AEFT", "AETF", "AFET", "AFTE", "TEAF", "TEFA", "TAEF", "TAFE", "TFEA", "TFAE"]],
    "game2": [["count", "W", "L"], ["sum"], ["sum"], ["sum"], ["sum"]],
    "game3": [["count", "W", "L"], ["skip"]],
    "game4": [["count", "W", "L"], ["count"], ["count"]],
    "game5": [["count", "W", "L"], ["count"]],
}
OUTPUT_HEADERS = {
    "fullExperimentalTrials1": ["W", "L", "game1plays", "game2plays", "game3plays", "game4plays", "game5plays"],
    "fullExperimentalTrials2": ["W", "L", "game1plays", "game2plays", "game3plays", "game4plays", "game5plays"],
    "fullExperimentalTrials3": ["W", "L", "game1plays", "game2plays", "game3plays", "game4plays", "game5plays"],
    "game1": ["W", "L",
        'AEFT', 'AETF', 'AFET', 'AFTE', 'ATEF', 'ATFE', 
        'EAFT', 'EATF', 'EFAT', 'EFTA', 'ETAF', 'ETFA', 
        'FAET', 'FATE', 'FEAT', 'FETA', 'FTAE', 'FTEA', 
        'TAEF', 'TAFE', 'TEAF', 'TEFA', 'TFAE', 'TFEA', 
    ],
    "game2": ["W", "L", "Clubs", "Diamonds", "Hearts", "Spades"],
    "game3": ["W", "L"],
    "game4": ["W", "L", "1", "2", "3", "4", "5", "6"],
    "game5": ["W", "L", "1", "2", "3", "4", "5", "6", "7"],
}
OUTPUT_FILE_PREFIX = "output"
OUTPUT_FILE_SUFFIX = ""
OUTPUT_FILE_EXTENSION = ".csv"
EXPERIMENTAL_TRIAL_FOLDER_NAMES = [
    "fullExperimentalTrials1",
    "fullExperimentalTrials2",
    'fullExperimentalTrials3',
    "game1",
    "game2",
    "game3",
    "game4",
    "game5",
]
DATA_FOLDER = "data\\computerizedData"
DATA_FILE_EXTENSION = ".csv"


class Wywy(cmd.Cmd):
    intro = "Welcome to Wywy for Frog Jump Testing. Type help to list commands.\n"
    prompt = "Wywy (Frog Jump) >> "
    
    # commands:
    GAMES_TO_PLAY = ["full1", "full3", "1", "2", "3", "4", "5"] # "full2",
    FULL_GAME_ALIASES = {"-b": "batches"}
    FULL_GAME_TYPES = {"batches": int}
    def do_fullGame(self, arg):
        "Runs batches of 100,000 trials for every Frog Jump game and the entire Frog Jump game starting from both lily pad 1 and lily pad 2. Data is decimated afterwards. Specify the number of batches TO END WITH after the arg \"-b\". Arguments are also passed into the decimate function."
        args = self.parseArgs(arg, self.FULL_GAME_ALIASES, self.FULL_GAME_TYPES)
        
        if not "batches" in args:
            print("Wywy is sad that you didn't tell him how many batches to run.")
            return
        
        for i in self.GAMES_TO_PLAY:
            self.do_play(i + " " + str(args["batches"]))
        
        # decimate data afterwards
        self.do_decimate(arg)
    
    def do_play(self, arg):
        "Runs batches of 100,000 trials for entire or individual Frog Jump games (game number -> arg 1) (number of batches TO END WITH? -> arg 2). Only runs if the first arg is OK (arg = full, 1, 2, 3, 4, 5)."
        args = arg.split(" ")
        folderPath = EXPERIMENTAL_TRIAL_FOLDER + "\\"
        scriptPath = EXPERIMENTAL_TRIAL_FOLDER + "\\"
        csvHead = ""
        # ensure valid input
        match args[0]:
            # case "full" | "fullExperimentalTrials": # alias moment :P
            #     folderPath += "fullExperimentalTrials"
            #     scriptPath += "full.ts"
            case "full1" | "fullExperimentalTrials1":
                folderPath += "fullExperimentalTrials1"
                scriptPath += "fullExperimentalTrials1.ts"
                csvHead = CSV_HEADS["full1"]
            case "full2" | "fullExperimentalTrials2":
                folderPath += "fullExperimentalTrials2"
                scriptPath += "fullExperimentalTrials2.ts"
                csvHead = CSV_HEADS["full2"]
            case "full3" | "fullExperimentalTrials3":
                folderPath += "fullExperimentalTrials3"
                scriptPath += "fullExperimentalTrials3.ts"
                csvHead = CSV_HEADS["full3"]
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
        i = 1
        while i < numDatasets:
            if (os.path.isfile(folderPath + "output.csv")):
                # move old the file elsewhere
                f = open(folderPath + "output.csv", "r")
                data = f.read()
                while (os.path.isfile(folderPath + "output" + str(i) + ".csv")):
                    i += 1
                
                # avoid playing games if you don't need to
                if i >= numDatasets:
                    break
                print("Playing games... (folderPath = " + folderPath + ") dataset #" + str(i))
                f = open(folderPath + "output" + str(i) + ".csv", "w+")
                f.write(data)
                f.close()


            f = open(folderPath + "output.csv", "w+")
            f.write(csvHead)
            f.close()

            process = subprocess.run(["npx", "tsx", scriptPath], shell=True)
    
    DECIMATE_ARG_ALIASES = {
        "-d": "delete",
        "-m": "move",
    }
    DECIMATE_ARG_RETURNTYPES = {
        "delete": str,
        "move": str,
    }
    def do_decimate(self, arg):
        "Decimates all the experimental trial data and optionally deletes (contains argument \"-d\") or moves (contains argument \"-m\") the raw data files. Assume the arguments are case-sensitive."
        
        args = self.parseArgs(arg, self.DECIMATE_ARG_ALIASES, self.DECIMATE_ARG_RETURNTYPES)
        
        # Decimate the data.
        for i in EXPERIMENTAL_TRIAL_FOLDER_NAMES: # catch every folder,
            writeHeaders = False
            self.optional_folder_creation(os.path.join(DATA_FOLDER)) # ensure there exists a folder to write to.
            
            output = None
            # if the output file does not exist yet, remember to add the headers
            if not os.path.isfile(os.path.join(DATA_FOLDER, i + DATA_FILE_EXTENSION)):
                writeHeaders = True
            
            
            filePath = os.path.join(EXPERIMENTAL_TRIAL_FOLDER, i, OUTPUT_FILE_PREFIX + "" + OUTPUT_FILE_SUFFIX + OUTPUT_FILE_EXTENSION)
            
            # avoid edgecase where the trials don't exist:
            if not os.path.isfile(filePath):
                continue
            
            output = open(os.path.join(DATA_FOLDER, i + DATA_FILE_EXTENSION), "a+")
            # avoid edgecase
            if (writeHeaders and os.path.isfile(filePath)):
                output.write(",".join(OUTPUT_HEADERS[i]))
            
            counter = 0
            dataToWrite = {}
            while (os.path.isfile(filePath)): # catch every file,
                print("Decimating " + filePath + "...")
                # reset counting variables:
                dataToWrite = {}
                
                # open up the data
                with open(filePath) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    numRows = 0
                    headers = None
                    
                    for row in csv_reader:
                        if (numRows == 0): # skip first row (rip runtime)
                            numRows = 1
                            headers = row
                            continue
                        
                        for a in range(len(row)):
                            try:
                                match DECIMATION_METHODS[i][a][0]:
                                    case "count":
                                        try:
                                            dataToWrite[row[a]] += 1
                                        except KeyError:
                                            dataToWrite[row[a]] = 1
                                    case "sum":
                                        try:
                                            dataToWrite[headers[a]] += int(row[a])
                                        except KeyError:
                                            dataToWrite[headers[a]] = int(row[a])
                                    case "skip":
                                        pass
                                    case _:
                                        print("Wywy is mad that you told him to do a decimation method he doesn't know how to do.")
                                        return
                            except IndexError:
                                print("Wywy is mad because there is a length discrepancy between the decimation method and experimental trial output. Rememeber to use \"[\"skip\"]\" if you want to ignore a column.")
                                return

                        numRows += 1
                    
                    # I LOVE python in this very instant
                    # BRO WHAT THE HELL IS ",".join(array) EVEN MEAN???
                    output.write("\n" + ",".join(list(map(lambda x: str(dataToWrite[x]), OUTPUT_HEADERS[i]))))
                
                
                counter += 1
                filePath = os.path.join(EXPERIMENTAL_TRIAL_FOLDER, i, OUTPUT_FILE_PREFIX + str(counter) + OUTPUT_FILE_SUFFIX + OUTPUT_FILE_EXTENSION)
            output.close()
        
        if "move" in args:
            for i in EXPERIMENTAL_TRIAL_FOLDER_NAMES:
                # check if there is a folder to be moved
                if os.path.isdir(os.path.join(EXPERIMENTAL_TRIAL_FOLDER, i)):
                    # self.optional_folder_creation(os.path.join(DATA_FOLDER, i))
                    shutil.move(os.path.join(EXPERIMENTAL_TRIAL_FOLDER, i), os.path.join(DATA_FOLDER))
        
        if "delete" in args:
            for i in EXPERIMENTAL_TRIAL_FOLDER:
                try:
                    shutil.rmtree(os.path.join(EXPERIMENTAL_TRIAL_FOLDER, i))
                except: # TODO make this catch the one specific error that is expected to potentially arise (directory does not exist)
                    pass
        
        print("Decimation Successfully Completed.")

    def do_bye(self, arg):
        "Exit the Wywy CLI."
        print("Goodbye!")
        exit()
    
    # helper functions
    def parseArgs(self, arg: str, aliases: dict, types: dict) -> dict:
        """Parses command line arguments given a raw string.

        Args:
            arg (str): _description_
            aliases (dict): Aliases to the keys of this dictionary (arguments).
            types (dict): Expected return types of the keys. e.g. {"wywyness": int, "random attribute whose type doesn't matter": str}

        Returns:
            dict: A dictionary with pairs of arguments. The values will always be the string passed in afterwards, and None if the respective key was the last argument passed in. These values are only important when the program expects a value (if you're looking for if a user typed in the keywords, just use the "in" keyword). It is the responsibility of another script to cast the values to integers.
        """
        
        args = arg.split(" ")
        currentKey = None
        output: dict = {}
        
        for i in range(len(args)):
            # check for aliases
            if args[i] in aliases:
                currentKey = aliases[args[i]]
            else:
                currentKey = args[i]
            
            try:
                output[currentKey] = types[currentKey](args[i + 1])
            except KeyError:
                # invalid argument name
                # do not inform user about this (because most programs don't do that I guess)
                pass
            except IndexError:
                # edge-case with the last argument
                output[currentKey] = None
            except ValueError:
                # invalid input, LOL
                print("WARNING: Wywy has detected invalid input relating to this argument!: " + args[i])
        
        return output
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