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
            pattern = pattern.lower()
            WordList = Tokenize(pattern)
            Similarity = len(set(BagOfWords) & set(WordList)) / len(set(BagOfWords + WordList))
            SimilarityPercentage = Similarity * 100

            if Similarity > MaxSimilarity:
                MaxSimilarity = Similarity
                MostSimilarPattern = intent_class
            
            if SimilarityPercentage > 100:
                SimilarityPercentage = SimilarityPercentage/100
            
    print(f"Similarity: {SimilarityPercentage:.2f}%")

    if MostSimilarPattern:
        return MostSimilarPattern
    else:
        raise NoMatchingIntentError("No matching intent class found.")

def responsecompare(input_string, intents_file_path, intent_class):
    input_string = input_string.lower()
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
        response = response.lower()
        WordList = Tokenize(response)

        for InputWord in BagOfWords:
            for OutputWord in WordList:
                if InputWord == OutputWord:
                    Similarity += 1
#                    print("Match found!")

        OutofHundred = len(BagOfWords)  # Total number of words in the input
        Hundred = len(BagOfWords + WordList)  # Total number of words in both input and pattern

        SimilarityPercentage = (Similarity / Hundred) * 100  # Corrected calculation
        
        if Similarity > MaxSimilarity:
            MaxSimilarity = Similarity
            MostSimilarResponse = response
        
        if SimilarityPercentage > 100:
            SimilarityPercentage = SimilarityPercentage/100
        
    print(f"Similarity: {SimilarityPercentage:.2f}%")
    
    # Convert MSR back into original string
    for response in responses:
        lowresponse = response.lower()
        if lowresponse == MostSimilarResponse:
            MostSimilarResponse = response
    
    return MostSimilarResponse

