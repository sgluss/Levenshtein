from levenshtein import *
import math
import time
import sys

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
    trie = TrieNode(0)
    for word in vocab:
        WordCount += 1
        trie.insert(word)

    print("Read %d words" % (WordCount))

    # threadsafe memo
    manager = Manager()
    memo = manager.dict()

    totalDistance = 0

    # More processes will be better on larger inputs.
    # This must be balanced against the time it takes to spool up processes
    procCount = 4
    pool = Pool(processes=procCount)

    blockSize = int(math.ceil(len(input) / procCount))
    shardedInput = [input[i:i + blockSize] for i in range(0, len(input), blockSize)]

    res = []
    # build arguments for multiple processes
    args = [(shardedInput[i], memo, totalDistance, trie, i,) for i in range(0,procCount)]

    preProc = time.time()

    # distribute sharded tasks to pool processes, collate the results
    for result in pool.starmap(runShardedInputOnTrie, args):
        totalDistance += result

    end = time.time()

    print("Preprocessing took %g s" % (preProc - start))
    print("Search took %g s" % (end - preProc))

    print("Total distance: " + str(totalDistance))

# Prevent subprocesses from executing main code
if __name__ == '__main__':

    # Use user supplied inputFile if one is provided. Otherwise, use the default
    if len(sys.argv) == 2:
        inputFile = sys.argv[1]
    else:
        inputFile = TEST_INPUT_FILE

    runInputOnTrie(TEST_INPUT_FILE, VOCAB_FILE)