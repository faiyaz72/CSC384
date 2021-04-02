# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

emissionTable = dict()
posCountTable = dict()
stateSpace = []
observationSpace = []

transitionTable = dict()
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

def populateTransitionTable(pos1, pos2):
    if (pos1 not in transitionTable):
        transitionTable[pos1] = dict()
        transitionBucket = transitionTable.get(pos1)
        transitionBucket[pos2] = 1
        transitionBucket['total'] = 1
        stateSpace.append(pos1)
    else:
        transitionBucket = transitionTable.get(pos1)
        if (pos2 not in transitionBucket):
            transitionBucket[pos2] = 1
        else:
            transitionBucket[pos2] = transitionBucket[pos2] + 1
        transitionBucket['total'] = transitionBucket['total'] + 1



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

    for word in emissionTable:
        posBucket = emissionTable.get(word)
        for pos in posBucket:
            posCount = posCountTable[pos]
            posBucket[pos] = posBucket[pos]/posCount

    for pos in transitionTable:
        transitionBucket = transitionTable.get(pos)
        total = transitionBucket['total']
        for transition in transitionBucket:
            if (transition != "total"):
                transitionBucket[transition] = transitionBucket[transition]/total
    
    test = open(test_file, "r")
    while True: 
        testLine = test.readline()
        if (not testLine):
            break
        parse = testLine.split()
        observationSpace.append(parse[0])

    probTrellis = np.zeros((len(stateSpace), len(observationSpace)))
    pathTrellis = np.empty((len(stateSpace), len(observationSpace)), dtype=object)

    for s in range(len(stateSpace)):
        emissionProbBucket = emissionTable[observationSpace[0]]
        probValue = 0
        if (stateSpace[s] in emissionProbBucket):
            probValue = emissionProbBucket[stateSpace[s]]
        probTrellis[s,0] = probValue
        pathTrellis[s,0] = stateSpace[s]

    # for o in range(1, len(observationSpace)):
    #     for s in range(len(stateSpace)):
            
    #         # x = np.argmax(x in probTrellis[x, o-1])
    
    print("initial done")



    
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