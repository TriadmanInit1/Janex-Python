from Janex import *

input_string = input("You: ")

words = Tokenize(input_string)

intents_file_path = "intents.json"

intent_class = patterncompare(input_string, intents_file_path)

BestResponse = responsecompare(input_string, intents_file_path, intent_class)

print(BestResponse)

stemmed_words = stem_sentence(input_string)
# print(stemmed_words)
