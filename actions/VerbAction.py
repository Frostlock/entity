from Action import Action

COMMANDS_SEARCH = ["google", "find", "search"]

from textblob import TextBlob, Word

import webbrowser

KEYWORD_DEFINE = "define"
KEYWORD_SEARCH = "search"

class VerbAction(Action):

    def __init__(self):
        pass

    @staticmethod
    def define(textBlob, verbIndex):
        VerbAction.log("AI: Define")

        for w , pos  in textBlob.tags[verbIndex + 1:]:
            w = Word(w)
            defs = []
            if pos[-1] == "S": w = w.singularize()
            if pos[0:2] == "NN": defs += w.define("n")
            elif pos[0:2] == "VB": defs += w.define("v")
            elif pos[0:2] == "JJ": defs += w.define("a")
            elif pos[0:2] == "RB": defs += w.define("a")
            else:
                # If none of the above trigger we are not going to define the word
                continue

            if len(defs) == 1:
                msg = w + ": " + defs[0]
            elif len(defs) > 1:
                msg = w + " has multiple meanings. "
                for d in defs:
                    msg += w + ": " + d + ". "
            else:
                msg = "I don't know what '" + w + "' means."

            return msg

    @staticmethod
    def search(textBlob, verbIndex):
        VerbAction.log("AI: Search")
        b = TextBlob(" ".join(textBlob.words[verbIndex + 1:]))

        np = b.noun_phrases
        if len(np) == 1:
            answer = "Searching Google for " + np[0] + "."
            url = "http://www.google.com/?#q=" + np[0]
            webbrowser.open(url=url, new=1, autoraise=True)
        else:
            answer = "Multiple noun phrases detected, not sure what to look for."
        return answer

    """
    Process instruction, return true if action was taken
    """
    @staticmethod
    def process(text_blob):
        # Get POS Part Of Speech tags
        tags = text_blob.tags
        print tags
        if len (text_blob.words) < 3 :
            print "Less than three words, can't work with that."
            return ""
        # Get the verb
        verbs = [x[0] for x in tags if x[1][:2] == "VB"]
        print verbs
        if (len(verbs) == 0):
            #TextBlob did not identify a verb. Maybe the second word is one?
            if len(Word(text_blob.words[1]).define('v')) > 0:
                verb = Word(text_blob.words[1])
            else:
                print "no verbs = no action."
                return ""
        elif (len(verbs) == 1):
            verb = Word(verbs[0])
        else:
            print "multiple verbs, don't know what to do."
            return ""

        verbIndex = [text_blob.words.index(x) for x in text_blob.words if x == verb][0]
        print "Verb detected: " + verb + " position " + str(verbIndex)

        # Get synonyms for the verb
        verbsyns = []
        for ss in verb.get_synsets(pos="v"):
            verbsyns = verbsyns + [s for s in ss.lemma_names() if not s in verbsyns]
        print verbsyns

        if KEYWORD_DEFINE in verbsyns:
            answer = VerbAction.define(text_blob, verbIndex)
        elif KEYWORD_SEARCH in verbsyns:
            answer = VerbAction.search(text_blob, verbIndex)
        else:
            return ""
        return answer


if __name__ == "__main__":
    b = TextBlob("Computer define killer rabbit")
    print b.noun_phrases
    b = TextBlob("Computer search for monty python")
    print b.noun_phrases
    VerbAction.process(b)
    print "THIS NEEDS TO BE REWRITTEN TO TAKE INTO ACCOUNT STRING RETURNS FROM process() CALL"
