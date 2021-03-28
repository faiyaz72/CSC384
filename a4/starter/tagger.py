# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys

emissionTable = dict()
posCountTable = dict()

def updatePosCount(pos):
    if (pos not in posCountTable):
        posCountTable[pos] = 1
    else:
        posCountTable[pos] = posCountTable[pos] + 1

def populateEmissionTable(word, pos):
    if (word not in emissionTable):
        emissionTable[word] = dict()
        posBucket = emissionTable.get(word)
        posBucket[pos] = 1
    else:
        posBucket = emissionTable.get(word)
        if (pos not in posBucket):
            posBucket[pos] = 1
        else:
            posBucket[pos] = posBucket[pos] + 1

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    for file in training_list:
        training = open(file, "r")
        while True:
            line = training.readline()
            if not line:
                break
            lineList = line.split()
            word = lineList[0]
            pos = lineList[-1]

            populateEmissionTable(word, pos)
            updatePosCount(pos)
    
    for word in emissionTable:
        posBucket = emissionTable.get(word)
        for pos in posBucket:
            posCount = posCountTable[pos]
            posBucket[pos] = posBucket[pos]/posCount


    
    print("File read")







if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)