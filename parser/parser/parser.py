import nltk
import string
import sys

#nltk.download('punkt')


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""



NONTERMINALS = """
S -> PART | PART Conj PART
PART -> NP VP | NP Adv VP | VP
NP -> N | NA N
NA -> Det | Adj | NA NA
VP -> V | V SUPP
SUPP -> NP | P | Adv | SUPP SUPP | SUPP SUPP SUPP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lower_sentence = sentence.lower()
    tokens = nltk.word_tokenize(lower_sentence)
    result = [ token for token in tokens if any(c.isalpha() for c in token)]
    return result
    # words = [word.lower() for word in nltk.word_tokenize(sentence)
    #               if any([c.isalpha() for c in word])]
    # return words



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    result = []
    for subtree in tree.subtrees(lambda x : x.label() == "NP"):
        if not any(sub_subtree for sub_subtree in subtree.subtrees() if sub_subtree.label() == "NP" and sub_subtree != subtree):
            result.append(subtree)
    return result
  




if __name__ == "__main__":
    main()
