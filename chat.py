from Janex import *

intents_file_path = "intents.json"
matcher = IntentMatcher(intents_file_path)

input_string = input("You: ")
words = matcher.Tokenize(input_string)

intent_class = matcher.patterncompare(input_string)

print(intent_class.get("tag"))

best_response = matcher.responsecompare(input_string, intent_class)

print(best_response)

stemmed_words = matcher.stem_sentence(input_string)
