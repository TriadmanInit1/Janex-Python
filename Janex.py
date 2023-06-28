import json
import string

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
    MostSimilarPattern = ""

    patterns = []
    Similarity = 0

    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)
    BagOfWords = Tokenize(input_string)
    for intent_class in intents['intents']:
        patterns = intent_class.get('patterns')
        for pattern in patterns:
            WordList = Tokenize(pattern)
            for word in WordList:
                if word in BagOfWords:
                    Similarity = Similarity + 1
                    print(Similarity)
            
            if Similarity > MaxSimilarity:
                MaxSimilarity = Similarity
                MostSimilarPattern = pattern
    
    return MostSimilarPattern

def responsecompare(input_string, intents_file_path, intent_class):
    MaxSimilarity = 0
    MostSimilarResponse = ""

    responses = []
    Similarity = 0

    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

    BagOfWords = Tokenize(input_string)
    
    responses = intent_class.get('responses')

    for response in responses:
        WordList = Tokenize(response)
        for word in WordList:
            if word in BagOfWords:
                Similarity = Similarity + 1
                print(Similarity)
            
        if Similarity > MaxSimilarity:
            MaxSimilarity = Similarity
            MostSimilarResponse = response
    
    return MostSimilarResponse



