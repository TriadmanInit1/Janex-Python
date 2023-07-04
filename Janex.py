import json
import string

class NoMatchingIntentError(Exception):
    pass

def Tokenize(input_string):
    input_string = input_string.strip()
    input_string = input_string.translate(str.maketrans("", "", string.punctuation))
    words = input_string.split()

    return words

def train(intents_file_path):
    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

def patterncompare(input_string, intents_file_path):
    input_string = input_string.lower()
    HighestSimilarity = 0
    MostSimilarPattern = None
    SimilarityPercentage = 0

    patterns = []
    Similarity = 0

    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

    WordList2 = Tokenize(input_string)

    for intent_class in intents['intents']:
        OverallWordList = []
        Similarity = 0

        patterns = intent_class.get('patterns')
        for pattern in patterns:
            WordList = []
            pattern = pattern.lower()
            WordList = Tokenize(pattern)
            OverallWordList.append(WordList)
            NewList = []
            NewBag = []

            for word in WordList:
                word = stem(word)
                NewList.append(word)

            for word in WordList2:
                word = stem(word)
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
        raise NoMatchingIntentError("No matching intent class found.")

def responsecompare(input_string, intents_file_path, intent_class):
    input_string = input_string.lower()
    HighestSimilarity = 0
    SimilarityPercentage = 0
    MostSimilarResponse = None

    responses = []
    Similarity = 0

    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

    WordList2 = Tokenize(input_string)

    if intent_class is not None:
        responses = intent_class.get('responses')
    else:
        raise NoMatchingIntentError("No matching intent class found.")

    for response in responses:

        Similarity = 0
        pattern = response.lower()
        WordList = Tokenize(response)
        NewList = []
        NewBag = []

        for word in WordList:
            word = stem(word)
            NewList.append(word)

        for word in WordList2:
            word = stem(word)
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

    # Convert MSR back into original string
    for response in responses:
        lowresponselist = []
        lowresponse = response.lower()
        lowresponselist = stem_sentence(lowresponse)

        for lowresponse in lowresponselist:
            if lowresponse == MostSimilarResponse:
                MostSImilarResponse = response

    return MostSimilarResponse

def stem(input_word):
    suffixes = ['ing', 'ly', 'ed', 'es', "'s", 'er', 'est', 'y', 'ily', 'able', 'ful', 'ness', 'less', 'ment', 'ive', 'ize', 'ous']
    for suffix in suffixes:
        if input_word.endswith(suffix):
            input_word = input_word[:-len(suffix)]
            break
    return input_word

def stem_sentence(input_string):
    wordlist = []
    stemmedwords = []
    wordlist = input_string.split()
    for input_word in wordlist:
        word = stem(input_word)
        stemmedwords.append(word)

    return stemmedwords
