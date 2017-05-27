# Added by Samuel Gluss 5/9/2017

# function to compute levenshtein distance
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

    while (x + 3) < m:
        e1 = ord(t[x])
        e2 = ord(t[x + 1])
        e3 = ord(t[x + 2])
        e4 = ord(t[x + 3])
        c = x
        b = x + 1
        d = x + 2
        g = x + 3
        h = x + 4
        x += 4
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

# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

    def insert(self, word):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word

# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search(word, maxCost, trie):

    # build first row
    currentRow = range( len(word) + 1 )

    results = [None, None]

    # recursively search each branch of the trie
    for letter in trie.children:
        searchRecursive( trie.children[letter], letter, word, currentRow,
            results, maxCost )

    return results

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive( node, letter, word, previousRow, results, maxCost ):
    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in range( 1, columns ):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 1
        else:
            replaceCost = previousRow[ column - 1 ]

        currentRow.append( min( insertCost, deleteCost, replaceCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost[0] and node.word != None:
        if (currentRow[-1] < maxCost[0]):
            maxCost[0] = currentRow[-1]
            results[0] = [node.word, currentRow[-1]]
    # if any entries in the row are less than the maximum cost, then
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost[0]:
        for letter in node.children:
            searchRecursive( node.children[letter], letter, word, currentRow,
                results, maxCost )
