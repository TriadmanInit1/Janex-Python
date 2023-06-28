from Janex import *

input_string = input("You: ")

words = Tokenize(input_string)

print(words)

intents_file_path = "intents.json"

intent_class = patterncompare(input_string, intents_file_path)

print(intent_class)

BestResponse = responsecompare(input_string, intents_file_path, intent_class)

print(BestResponse)