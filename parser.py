import nltk
import sys

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
S -> NP | NP VP | VP NP | NP VP NP | NP VP NP Adv | S Conj S
NP -> N | Det N | Adj NP | Det Adj NP | NP P NP| P NP
VP -> V | Adv VP | P VP | VP Adv
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
    nltk.download("punkt")

    words = nltk.word_tokenize(
        text=sentence
    )

    lowercases = []
    for word in words:
        if not word.isalpha():
            continue

        lowercases.append(word.lower())

    return lowercases


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    nounPhrases = []
    queue: list = tree

    while len(queue) > 0:
        queue_item = queue.pop(0)

        label = queue_item.label()

        if label == 'VP' or label == 'Conj':
            continue

        npCounter = 0
        for subtree in queue_item:
            if type(subtree) is str:
                continue

            subtree_label = subtree.label()

            if subtree_label != "NP":
                continue

            npCounter += 1

        if npCounter < 1 and label == "NP":
            nounPhrases.append(queue_item)
        else:
            for subtree in queue_item:
                if type(subtree) is str:
                    continue

                queue.append(subtree)

            

    return nounPhrases


if __name__ == "__main__":
    main()
