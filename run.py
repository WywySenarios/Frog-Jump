import os
import csv
import cmd
import subprocess

EXPERIMENTAL_TRIAL_FOLDER = "experimentalTrials"
CSV_HEADS = {
    "full1": "result,game1plays,game2plays,game3plays,game4plays,game5plays",
    "full2": "result,game1plays,game2plays,game3plays,game4plays,game5plays",
    "1": "result,letters",
    "2": "result,Clubs,Diamonds,Hearts,Spades",
    "3": "result,letters",
    "4": "result,roll1,roll2",
    "5": "result,roll",
}
DECIMATION_METHODS = {
    "fullExperimentalTrials1": [["count", "W", "L"], ["sum"], ["sum"], ["sum"], ["sum"], ["sum"]],
    "fullExperimentalTrials2": [["count", "W", "L"], ["sum"], ["sum"], ["sum"], ["sum"], ["sum"]],
    "game1": [["count", "W", "L"], ["count", "EFTA", "EFAT", "ETAF", "ETFA", "EFA", "FAET", "FATE", "FEAT", "FETA", "FTAE", "FTEA", "ATEF", "ATFE", "AEFT", "AETF", "AFET", "AFTE", "TEAF", "TEFA", "TAEF", "TAFE", "TFEA", "TFAE"]],
    "game2": [["count", "W", "L"], ["sum"], ["sum"], ["sum"], ["sum"]],
    "game3": [["count", "W", "L"], ["skip"]],
    "game4": [["count", "W", "L"], ["count"], ["count"]],
    "game5": [["count", "W", "L"], ["count"]],
}
OUTPUT_HEADERS = {
    "fullExperimentalTrials1": ["W", "L", "game1plays", "game2plays", "game3plays", "game4plays", "game5plays"],
    "fullExperimentalTrials2": ["W", "L", "game1plays", "game2plays", "game3plays", "game4plays", "game5plays"],
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
    
    def do_play(self, arg):
        "Runs batches of 100,000 trials for entire or individual Frog Jump games (game number -> arg 1) (number of batches? -> arg 2). Only runs if the first arg is OK (arg = full, 1, 2, 3, 4, 5)."
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
    
    def do_decimate(self, arg):
        "Decimates all the experimental trial data and optionally deletes (argument == \"True\") or moves (arugment == \"Move\") the raw data files. Assume the arguments are case-sensitive."
        
        # Decimate the data.
        for i in EXPERIMENTAL_TRIAL_FOLDER_NAMES: # catch every folder,
            writeHeaders = False
            self.optional_folder_creation(os.path.join(DATA_FOLDER)) # ensure there exists a folder to write to.
            
            output = None
            # if the output file does not exist yet, remember to add the headers
            if not os.path.isfile(os.path.join(DATA_FOLDER, i + DATA_FILE_EXTENSION)):
                writeHeaders = True
            output = open(os.path.join(DATA_FOLDER, i + DATA_FILE_EXTENSION), "a+")
            
            
            filePath = os.path.join(EXPERIMENTAL_TRIAL_FOLDER, i, OUTPUT_FILE_PREFIX + "" + OUTPUT_FILE_SUFFIX + OUTPUT_FILE_EXTENSION)
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

    def do_bye(self, arg):
        "Exit the Wywy CLI."
        print("Goodbye!")
        exit()
    
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