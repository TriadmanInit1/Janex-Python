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
    MaxSimilarity = 0
    MostSimilarPattern = None

    patterns = []
    Similarity = 0

    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

    BagOfWords = Tokenize(input_string)

    for intent_class in intents['intents']:
        
        patterns = intent_class.get('patterns')
        for pattern in patterns:
            WordList = Tokenize(pattern)
            Similarity = len(set(BagOfWords) & set(WordList)) / len(set(BagOfWords + WordList))
            SimilarityPercentage = Similarity * 100

            if Similarity > MaxSimilarity:
                print(f"Similarity: {SimilarityPercentage:.2f}%")
                MaxSimilarity = Similarity
                MostSimilarPattern = intent_class

    if MostSimilarPattern:
        return MostSimilarPattern
    else:
        raise NoMatchingIntentError("No matching intent class found.")

def responsecompare(input_string, intents_file_path, intent_class):
    MaxSimilarity = 0
    MostSimilarResponse = None

    responses = []
    Similarity = 0

    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

    BagOfWords = Tokenize(input_string)

    if intent_class is not None:
        responses = intent_class.get('responses')
    else:
        raise NoMatchingIntentError("No matching intent class found.")

    for response in responses:
        WordList = Tokenize(response)
        Similarity = len(set(BagOfWords) & set(WordList)) / len(set(BagOfWords + WordList))
        SimilarityPercentage = Similarity * 100

        if Similarity > MaxSimilarity:
            print(f"Similarity: {SimilarityPercentage:.2f}%")
            MaxSimilarity = Similarity
            MostSimilarResponse = response
    
    if MostSimilarResponse:

        return MostSimilarResponse
    
    else:

        raise NoMatchingIntentError("No matching response found.")
