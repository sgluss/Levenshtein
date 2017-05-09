from levenshtein import levenshtein

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

def getDistanceOfSentence(words, vocab, memo):
    totalDistance = 0
    distance = float("inf")
    tempDistance = distance
    tempWord = ""

    for word in words:
        # if word distance has already been calculated, use that
        if word in memo:
            totalDistance += memo[word]
        else:
            for vocabWord in vocab:
                if distance == 0:
                    break

                # only calculate levenshtein distance if the word lengths are closer than the shortest distance seen so far
                if abs(len(word) - len(vocabWord)) < distance:
                    tempDistance = levenshtein(word, vocabWord)
                    if (tempDistance < distance):
                        distance = tempDistance
                        tempWord = vocabWord

            totalDistance += distance
            memo[word] = distance
            distance = float("inf")

    return totalDistance

def runOnInput(inputFile):
    # read in vocab and input
    vocabulary = open("vocabulary.txt", "r").read().lower().split('\n')
    testInput = open(inputFile, "r").read().lower()

    # Sanitize and split the input into an array of words
    testInput = sanitizeInputString(testInput).split(" ")

    # memoize results just in case we happen to see the same mispelling more than once
    memo = {}

    print("expected: " + str(levenshtein("tihs", "this") +
    levenshtein("sententcnes", "sentence") +
    levenshtein("iss", "is") +
    levenshtein("nout", "not") +
    levenshtein("varrry", "very") +
    levenshtein("goud", "good")))

    print("result: " + str(getDistanceOfSentence(testInput, vocabulary, memo)))

# execute tests and input
runTests()
runOnInput("example_input")