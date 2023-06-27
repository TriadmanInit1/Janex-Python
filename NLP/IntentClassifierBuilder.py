import json
import Tokenizer

with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

def train(intents_file_path):
    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)

def intentcompare(input_string, intents_file_path):
    MaxSimilarity = 0
    MostSimilarPattern = ""

    patterns = []
    Similarity = 0

    with open(intents_file_path, 'r') as json_data:
        intents = json.load(json_data)
    BagOfWords = Tokenize(input_string)
    for intent_class in intents['intents']:
        patterns = intent_class.get("patterns")
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





