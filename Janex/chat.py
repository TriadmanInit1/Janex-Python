from main import *

intents_file_path = "./intents.json"
thesaurus_file_path = "./thesaurus.json"

matcher = IntentMatcher(intents_file_path, thesaurus_file_path)

input_string = input("You: ")

intent_class, percentage = matcher.pattern_compare(input_string)
response = matcher.response_compare(input_string, intent_class)

response = matcher.ResponseGenerator(response)

print(response)
