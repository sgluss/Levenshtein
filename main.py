from levenshtein import *
import math
import time

# Check if input char is one which
def isAllowedChar(char):
    val = ord(char)
    # if char A-Z, a-z, or space then return true
    if (val > 96 and val < 123) or val == 32:
        return char
    else:
        return ""

# input is a string which may have duplicate spaces in it
def sanitizeInputString(input):
    retVal = isAllowedChar(input[0])

    for i in range(0,len(input) - 1):
        if input[i] != ' ' or input[i+1] != ' ':
            retVal += isAllowedChar(input[i + 1])
    return retVal

def runTests():
    # Result is expected to be 1
    test1 = levenshtein("bat", "fat")
    test2 = levenshtein("bat", "fated")
    test3 = levenshtein("sententcnes", "centner")
    print(test1)
    print(test2)
    # Failing
    print(test3)

# Input is a list of strings
def indexListByWordLength(list):
    retVal = {}
    for string in list:
        length = len(string)
        if length not in retVal:
            retVal[length] = []
        retVal[length] += [string]
    return retVal

def iterateIndex(counter, length):
    # Set index to next nearest value to word length
    return length + math.ceil(counter / 2) if counter % 2 else length - math.ceil(counter / 2)

def getDistanceOfWordFromVocab(word, vocab, memo):
    distance = len(word)
    tempDistance = distance
    tempWord = ""

    length = len(word)
    index = length
    counter = 0
    # only consider words which have a possibility of producing a smaller distance
    while (abs(index - length) < distance):
        if index not in vocab:
            counter += 1
            index = iterateIndex(counter, length)
            continue

        for vocabWord in vocab[index]:
            if distance == 0:
                memo[word] = 0
                return 0

            # only calculate levenshtein distance if the word lengths are closer than the shortest distance seen so far
            if abs(len(word) - len(vocabWord)) < distance:
                tempDistance = levenshtein(word, vocabWord)
                if (tempDistance < distance):
                    distance = tempDistance
                    tempWord = vocabWord
        counter += 1
        index = iterateIndex(counter, length)

    memo[word] = distance
    return distance

def getDistanceOfSentence(words, vocab, memo):
    totalDistance = 0

    for word in words:
        # if word distance has already been calculated, use that
        if word in memo:
            totalDistance += memo[word]
        else:
            totalDistance += getDistanceOfWordFromVocab(word, vocab, memo)

    return totalDistance

def runOnInput(inputFile):
    # read in vocab and input
    vocabulary = open("vocabulary.txt", "r").read().lower().split('\n')
    testInput = open(inputFile, "r").read().lower()

    # Sanitize and split the input into an array of words
    testInput = sanitizeInputString(testInput).split(" ")

    vocabulary = indexListByWordLength(vocabulary)

    # memoize results just in case we happen to see the same mispelling more than once
    memo = {}

    print("expected: " + str(levenshtein("tihs", "this") +
    levenshtein("sententcnes", "sentence") +
    levenshtein("iss", "is") +
    levenshtein("nout", "not") +
    levenshtein("varrry", "very") +
    levenshtein("goud", "good")))

    start = time.clock()
    print("result: " + str(getDistanceOfSentence(testInput, vocabulary, memo)))
    end = time.clock()
    print("Time to complete: " + str(end - start) + " seconds")

# execute tests and input
runTests()
runOnInput("187")