
# function to computer levenshtein distance
# see code here: https://jsperf.com/levenshtein-algorithms/27
# this algo is the fastest of the 10, levenshtein10()
def levenshtein(s, t):
    if (s == t):
        return 0

    n = len(s)
    m = len(t)

    if (n == 0 or m == 0):
        return n + m

    x, y, a, b, c, d, g, h = 0, 0, 0, 0, 0, 0, 0, 0
    p = [x+1 for x in range(n)]

    for x in range(0, m - 3, 4):
        e1 = ord(t[x])
        e2 = ord(t[x + 1])
        e3 = ord(t[x + 2])
        e4 = ord(t[x + 3])
        c = x
        b = x + 1
        d = x + 2
        g = x + 3
        h = x + 4
        for y in range(0, n):
            f = ord(s[y])
            a = p[y]
            if (a < c or b < c):
                c = (b + 1 if a > b else a + 1)
            elif (e1 != f):
                c += 1

            if (c < b or d < b):
                b = (d + 1 if c > d else c + 1)
            elif (e2 != f):
                    b += 1

            if (b < d or g < d):
                d = (g + 1 if b > g else b + 1)
            elif (e3 != f):
                    d += 1

            if (d < g or h < g):
                g = (h + 1 if d > h else d + 1)
            elif (e4 != f):
                    g += 1

            p[y] = h = g
            g = d
            d = b
            b = c
            c = a

    while x < m:
        e = ord(t[x])
        c = x
        x += 1
        d = x
        for y in range(0, n):
            a = p[y]
            if (a < c or d < c):
                d = (d + 1 if a > d else a + 1)
            else:
                if (e != ord(s[y])):
                    d = c + 1
                else:
                    d = c
            p[y] = d
            c = a
        h = d

    return h

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


runTests()

# read in vocab and input
vocabulary = open("vocabulary.txt", "r").read().lower().split('\n')
testInput = open("example_input", "r").read().lower()

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