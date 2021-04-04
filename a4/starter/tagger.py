# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np
from numpy.lib import tracemalloc_domain

emissionTable = dict()
posCountTable = dict()
stateSpace = []
observationSpace = []
transitionTable = dict()
transitionCount = dict()

def updatePosCount(pos):
    if (pos not in posCountTable):
        posCountTable[pos] = 1
        stateSpace.append(pos)
    else:
        posCountTable[pos] = posCountTable[pos] + 1

def populateEmissionTable(word, pos):
    key = word + " | " + pos 
    if (key not in emissionTable):
        emissionTable[key] = 1
    else:
        emissionTable[key] = emissionTable[key] + 1

def populateTransitionTable(pos1, pos2):
    key = pos1 + " | " + pos2 
    if (key not in transitionTable):
        transitionTable[key] = 1
    else:
        transitionTable[key] = transitionTable[key] + 1
    
    if pos1 not in transitionCount:
        transitionCount[pos1] = 1
    else:
        transitionCount[pos1] = transitionCount[pos1] + 1



def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    for file in training_list:
        training = open(file, "r")
        currentLine = training.readline()
        if (currentLine):
            nextLine = training.readline()
        else:
            nextLine = None

        while True:
            if not currentLine:
                break
            lineList1 = currentLine.split()
            word1 = lineList1[0]
            pos1 = lineList1[-1]
            populateEmissionTable(word1, pos1)
            updatePosCount(pos1)

            if (nextLine):
                lineList2 = nextLine.split()
                pos2 = lineList2[-1]                
                populateTransitionTable(pos1, pos2)


            currentLine = nextLine
            nextLine = training.readline()

    for pair in emissionTable:
        parse = pair.split()
        pos = parse[-1]
        emissionTable[pair] = emissionTable[pair]/posCountTable[pos]

    for pair in transitionTable:
        parse = pair.split()
        total = transitionCount[parse[0]]
        transitionTable[pair] = transitionTable[pair]/total
    
    test = open(test_file, "r")
    while True: 
        testLine = test.readline()
        if (not testLine):
            break
        parse = testLine.split()
        observationSpace.append(parse[0])
    
    emissionPath = []
    for observation in observationSpace:
        maxProb = 0
        maxState = None
        for state in stateSpace:
            key = observation + " | " + state
            if (key in emissionTable):
                if (emissionTable[key] > maxProb):
                    maxProb = emissionTable[key]
                    maxState = state
        if (not maxState):
            maxState = stateSpace[np.randint(0, len(stateSpace) - 1)]
        emissionPath.append(maxState)

    print(emissionPath)
    # probTrellis = np.zeros((len(stateSpace), len(observationSpace)))
    # pathTrellis = np.empty((len(stateSpace), len(observationSpace)), dtype=object)

    # for s in range(len(stateSpace)):
    #     probValue = 0
    #     key = observationSpace[0] + " | " + stateSpace[s]
    #     if (key in emissionTable):
    #         probValue = emissionTable[key]
    #     probTrellis[s,0] = probValue
    #     pathTrellis[s,0] = stateSpace[s]

    # for o in range(1, len(observationSpace)):
    #     maxProb = []
    #     for s in range(len(stateSpace)):
    #         # x = np.argmax(x in probTrellis[x, o-1] * transitionTable[pathTrellis[x][o-1] + " | " + stateSpace[s]] * emissionTable[observationSpace[o] + " | " + stateSpace[s]])
    #         maxIndex = []
    #         maxProb = []
    #         limit = probTrellis.shape
    #         for x in range(limit[0]):
    #             transitionKey = pathTrellis[x][o-1] + " | " + stateSpace[s]
    #             if (transitionKey not in transitionTable):
    #                 transition = 0
    #             else:
    #                 transition = transitionTable[pathTrellis[x][o-1] + " | " + stateSpace[s]]

    #             emissionKey = observationSpace[o] + " | " + stateSpace[s]
    #             if (emissionKey not in emissionTable):
    #                 emission = 0
    #             else:
    #                 emission = emissionTable[observationSpace[o] + " | " + stateSpace[s]]
    #             probability = probTrellis[x, o-1] * transition * emission
    #             maxProb.append(probability)
    #             maxIndex.append(st)
    #         print(x)



    
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