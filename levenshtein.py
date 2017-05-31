# Added by Samuel Gluss 5/9/2017

# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words. Current node length is also added to enable short-circuiting
class TrieNode:
    def __init__(self, length):
        self.word = None
        self.children = {}
        self.length = length

    def insert(self, word):
        node = self
        for index, letter in enumerate(word):
            if letter not in node.children:
                node.children[letter] = TrieNode(index + 1)

            node = node.children[letter]

        node.word = word

# The search function returns a list of all words that are less than the given
# maximum distance from the target word
# maxCost should be a list with one element, so that it can be modified as better matches are found
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
        # Short circuit if this recursive subtree word length difference is worse than the current best match distance
        if node.length - len(word) < maxCost[0] - 1:
            for letter in node.children:
                searchRecursive( node.children[letter], letter, word, currentRow,
                    results, maxCost )
