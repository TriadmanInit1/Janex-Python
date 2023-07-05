import json
import string

class IntentMatcher:
    def __init__(self, intents_file_path):
        self.intents_file_path = intents_file_path
        self.intents = self.train()

    class NoMatchingIntentError(Exception):
        pass

    def Tokenize(self, input_string):
        input_string = input_string.strip()
        input_string = input_string.translate(str.maketrans("", "", string.punctuation))
        words = input_string.split()

        words = self.stem_list(words)

        return words

    def Tokenize_List(self, input_list):
        Tokenwords = []
        for word in input_list:
            token = self.Tokenize(word)
            Tokenwords.append(token)

        return Tokenwords

    def train(self):
        with open(self.intents_file_path, 'r') as json_data:
            intents = json.load(json_data)
        return intents

    def patterncompare(self, input_string):
        input_string = input_string.lower()
        HighestSimilarity = 0
        MostSimilarPattern = None
        SimilarityPercentage = 0

        patterns = []
        Similarity = 0

        WordList2 = self.Tokenize(input_string)

        for intent_class in self.intents['intents']:
            OverallWordList = []
            Similarity = 0

            patterns = intent_class.get('patterns')
            for pattern in patterns:
                WordList = []
                pattern = pattern.lower()
                WordList = self.Tokenize(pattern)
                OverallWordList.append(WordList)
                NewList = []
                NewBag = []

                for word in WordList:
                    word = self.stem(word)
                    NewList.append(word)

                for word in WordList2:
                    word = self.stem(word)
                    NewBag.append(word)

                WordList = NewList
                WordList2 = NewBag

                for word in WordList2:
                    if word in WordList:
                        Similarity = Similarity + 1

                    if Similarity > HighestSimilarity:
                        SimilarityPercentage = Similarity / len(OverallWordList + WordList2)
                        HighestSimilarity = Similarity
                        MostSimilarPattern = intent_class

        print(f"Similarity: {SimilarityPercentage:.2f}%")

        if MostSimilarPattern:
            return MostSimilarPattern
        else:
            raise self.NoMatchingIntentError("No matching intent class found.")

    def responsecompare(self, input_string, intent_class):
        input_string = input_string.lower()
        HighestSimilarity = 0
        SimilarityPercentage = 0
        MostSimilarResponse = None

        responses = []
        Similarity = 0

        WordList2 = self.Tokenize(input_string)

        if intent_class is not None:
            responses = intent_class.get('responses')
        else:
            raise self.NoMatchingIntentError("No matching intent class found.")

        for response in responses:

            Similarity = 0
            pattern = response.lower()
            WordList = self.Tokenize(response)
            NewList = []
            NewBag = []

            for word in WordList:
                word = self.stem(word)
                NewList.append(word)

            for word in WordList2:
                word = self.stem(word)
                NewBag.append(word)

            WordList = NewList
            WordList2 = NewBag

            for word in WordList2:
                if word in WordList:
                    Similarity = (Similarity+1/len(WordList + WordList2))

                if Similarity > HighestSimilarity:
                    SimilarityPercentage = Similarity * 100
                    HighestSimilarity = Similarity
                    MostSimilarResponse = response

        print(f"Similarity: {SimilarityPercentage:.2f}%")

        # Convert MSR back into the original string
        for response in responses:
            lowresponselist = []
            lowresponse = response.lower()
            lowresponselist = self.stem_sentence(lowresponse)

            for lowresponse in lowresponselist:
                if lowresponse == MostSimilarResponse:
                    MostSimilarResponse = response

        return MostSimilarResponse

    def stem(self, input_word):
        suffixes = ['ing', 'ly', 'ed', 'es', "'s", 'er', 'est', 'y', 'ily', 'able', 'ful', 'ness', 'less', 'ment', 'ive', 'ize', 'ous']
        for suffix in suffixes:
            if input_word.endswith(suffix):
                input_word = input_word[:-len(suffix)]
                break
        return input_word

    def stem_sentence(self, input_string):
        wordlist = []
        stemmedwords = []
        wordlist = input_string.split()
        for input_word in wordlist:
            word = self.stem(input_word)
            stemmedwords.append(word)

        return stemmedwords

    def stem_list(self, input_list):
        stemmedwords = []
        for word in input_list:
            stemmedword = self.stem(word)
            stemmedwords.append(stemmedword)

        return stemmedwords
