"""
    Module senticnet
"""

import sys

class Senticnet:
    """ Class senticnet """

    def __init__(self, path="senticnet/senticnet.py"):
        """
            Loads a senticnet file into a dict.

            Usage :
            --------
            senticnet.Senticnet('path/to/file')

            (where senticnet is the name of this imported module)
        """

        self.senticnet = {}

        # Tries to open the file
        try:
            with open(path, 'r', encoding="utf-8") as senticnetFile:
                senticnetFile = senticnetFile.readlines()

                # Loops through each line
                for line in senticnetFile:
                    line = line.strip()

                    # Skips comments
                    if line [0] == '#':
                        pass
                    else:
                        # Tries to get the word
                        try:
                            # Gets the word
                            word = line.split("'] = [")[0].strip()
                            word = word.replace("senticnet['", '')

                            # Gets the value associated with the word
                            values = '[' + line.split("'] = [")[1]

                            # Adds to senticnet dict
                            # Unsafe (because of eval()), but I won't create
                            # a parser for the values...
                            self.senticnet[word] = eval(values)

                        # If something goes wrong (comment/wrong-formatted line/etc.)
                        except IndexError:
                            pass
                print(f"# Note : Senticnet successfully loaded with {len(self.senticnet)} entries.")
                return

        except IOError:
            print("# Note : Failed to load senticnet file. Aborting program.")
            sys.exit()
            return

    def polarityOf(self, word):
        """
            Returns the polarity associated with a word given as argument.
        """

        try:
            return float(self.senticnet[word][7])

        except KeyError:
            return None

    def introspectionOf(self, word):
        """
            Returns the introspection associated with a word given as argument.
        """

        try:
            return float(self.senticnet[word][0])

        except KeyError:
            return None

    def temperOf(self, word):
        """
            Returns the temper associated with a word given as argument.
        """

        try:
            return float(self.senticnet[word][1])

        except KeyError:
            return None

    def attitudeOf(self, word):
        """
            Returns the temper associated with a word given as argument.
        """

        try:
            return float(self.senticnet[word][2])

        except KeyError:
            return None

    def sensitivityOf(self, word):
        """
            Returns the sensitivity associated with a word given as argument.
        """

        try:
            return float(self.senticnet[word][3])

        except KeyError:
            return None

    def emotionsOf(self, word):
        """
            Returns the primary and secondary emotions associated
            with a word given as argument and returns a dict
            with the two emotions, if found.

            Usage :
            --------
            s.emotionsOf('word')

            (where s is a senticnet object)
        """

        try:
            # Finds primary and secondary emotion of the word
            primary_emotion = self.senticnet[word][4]
            secondary_emotion = self.senticnet[word][5]

            # Replaces # if the emotion is a string (and not None)
            if primary_emotion:
                primary_emotion = primary_emotion.replace('#', '')
            if secondary_emotion:
                secondary_emotion = secondary_emotion.replace('#', '')

            return {
                'primary_emotion':primary_emotion,
                'secondary_emotion':secondary_emotion
            }

        except KeyError:
            return {'primary_emotion':None, 'secondary_emotion':None}

    def synonymsOf(self, word):
        """
            Tries to find the synonyms of a word given as argument
            and returns a list of synonyms, if found.

            Usage :
            --------
            s.synonymsOf('word')

            (where s is a senticnet object)
        """

        try:
            return self.senticnet[word][8:]

        except KeyError:
            return []

    def reverseSearch(self, word):
        """
            Tries to find words that have for synonym
            the given word passed as argument, and
            returns a list of words, if found.

            Usage :
            --------
            s.reverseSearch('word')

            (where s is a senticnet object)
        """

        found_words = []

        # Loops through each entry of senticnet
        for word, _ in self.senticnet.items():
            # If word is found as synonym, add it to the list
            if word in self.synonymsOf(word):
                found_words.append(word)

        return found_words

    def averageEmotionsOf(self, words):
        """
            Tries to find and return the average primary and
            secondary emotions in a list of words or a string.

            It can takes as argument a str (single word) or
            a list (depending on the amount of words).

            It returns a dict with the primary and secondary
            emotions (average) associated with the str or list.

            Usage :
            -------
            s.averageEmotionsOf('word')
                OR
            s.averageEmotionsOf(['word1', 'word2', 'word3'])

            (where s is a senticnet object)
        """

        primary_emotions = {}
        secondary_emotions = {}

        # Converts to list, if needed
        if isinstance(words, str):
            words = [words]
        if not isinstance(words, str) and not isinstance(words, list):
            return {"primary_emotion":None, "secondary_emotion":None}

        # Loops through each word and find associated emotions
        for word in words:
            emotions = self.emotionsOf(word)

            # Stores each emotion for each word
            pe = emotions["primary_emotion"]
            se = emotions["secondary_emotion"]

            # Adds to dict for primary emotions
            if pe in primary_emotions:
                primary_emotions[pe] += 1
            else:
                primary_emotions[pe] = 1

            # Adds to dict for secondary emotions
            if se in secondary_emotions:
                secondary_emotions[se] += 1
            else:
                secondary_emotions[se] = 1

        # Sets None to -1 to avoid unusable outputs
        primary_emotions[None] = -1
        secondary_emotions[None] = -1

        # Finds average emotions
        if len(primary_emotions) > 0:
            primary_max = max(primary_emotions, key=primary_emotions.get)
        else:
            primary_max = None

        if len(secondary_emotions) > 0:
            secondary_max = max(secondary_emotions, key=secondary_emotions.get)
        else:
            secondary_max = None

        return {"primary_emotion":primary_max, "secondary_emotion":secondary_max}
