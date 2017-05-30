from levenshtein import *
import math
import time

from multiprocessing import Pool, Manager

TEST_INPUT_FILE = "187"
VOCAB_FILE = "vocabulary.txt"

# input is a single char
def isAllowedChar(char):
    val = ord(char)
    # if char a-z, or space then return true
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
    print(test3)

# Input is a list of strings
# Separate input into lists of words of a particular length, indexed by length
def indexListByWordLength(list):
    retVal = {}
    for string in list:
        length = len(string)
        if length not in retVal:
            retVal[length] = []
        retVal[length] += [string]
    return retVal

# Iterator to set an index to the next closest position to a word length
# EG for length 4, this function will iterate the index from 4 -> 5 -> 3 -> 6 -> 2 ...
def iterateIndex(counter, length):
    # Set index to next nearest value to word length
    return length + math.ceil(counter / 2) if counter % 2 else length - math.ceil(counter / 2)

def getDistanceOfWordFromVocab(word, vocab, memo):
    distance = len(word)
    tempDistance = distance
    # handy for debug
    tempWord = ""

    length = len(word)
    index = length
    counter = 0
    # only consider words which have a possibility of producing a smaller distance
    while (abs(index - length) < distance):
        # If there are no words of this length, try the next index
        if index not in vocab:
            counter += 1
            index = iterateIndex(counter, length)
            continue

        for vocabWord in vocab[index]:
            if distance == 0:
                # word match found
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

    # all reasonable possibilities have been explored, memoize/return the best match
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

def getSanitizedInputAndVocab(inputFile, vocabFile):
    # read in vocab and input
    vocab = open(vocabFile, "r").read().lower().split('\n')
    input = open(inputFile, "r").read().lower()

    # Sanitize and split the input into an array of words
    input = sanitizeInputString(input).split(" ")

    vocab = indexListByWordLength(vocab)

    return [input, vocab]

def runOnInput(inputFile, vocabFile):
    [testInput, vocabulary] = getSanitizedInputAndVocab(inputFile, vocabFile)

    # memoize results just in case we happen to see the same word/mispelling more than once
    memo = {}

    print("expected: " + "187")

    start = time.clock()
    print("result: " + str(getDistanceOfSentence(testInput, vocabulary, memo)))
    end = time.clock()
    print("Time to complete: " + str(end - start) + " seconds")

def runShardedInputOnTrie(input, memo, totalDistance, trie, worker):
    totalDistance = 0
    #print("worker " + str(worker) + " starting")
    for word in input:
        # if word distance has already been calculated, use that
        if word in memo:
            totalDistance += memo[word]
        else:
            maxLen = 0
            # algo does not work for maxLen vals under 2 (there is no vocab word with this length)
            if len(word) < 2:
                maxLen = 2
            else:
                maxLen = len(word)
            result = search(word, [maxLen], trie)
            memo[word] = result[0][1]
            totalDistance += result[0][1]
    #print("worker " + str(worker) + " finishing")
    return totalDistance

def runInputOnTrie(inputFile, vocabFile):
    start = time.time()

    # read in vocab and input
    vocab = open(vocabFile, "r").read().lower().split('\n')
    input = open(inputFile, "r").read().lower()

    # Sanitize and split the input into an array of words
    input = sanitizeInputString(input).split(" ")

    WordCount = 0

    # read dictionary file into a trie
    trie = TrieNode()
    for word in vocab:
        WordCount += 1
        trie.insert(word)

    print("Read %d words" % (WordCount))

    # threadsafe memo
    manager = Manager()
    memo = manager.dict()

    totalDistance = 0

    #add sharding code
    procCount = 4
    pool = Pool(processes=procCount)

    blockSize = int(math.ceil(len(input) / procCount))
    shardedInput = [input[i:i + blockSize] for i in range(0, len(input), blockSize)]

    res = []
    # Run multithreaded
    args = [(shardedInput[i], memo, totalDistance, trie, i,) for i in range(0,procCount)]

    preProc = time.time()

    for result in pool.starmap(runShardedInputOnTrie, args):
        totalDistance += result

    end = time.time()

    print("Preprocessing took %g s" % (preProc - start))
    print("Search took %g s" % (end - preProc))

    print("Total distance: " + str(totalDistance))

# Prevent subprocesses from executing main code
if __name__ == '__main__':
    # execute tests and input
    #runTests()
    #runOnInput(TEST_INPUT_FILE, VOCAB_FILE)
    runInputOnTrie(TEST_INPUT_FILE, VOCAB_FILE)