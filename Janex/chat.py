from main import *

intents_file_path = "./intents.json"
matcher = IntentMatcher(intents_file_path)

user_input = input("You: ")

intent_class, percentage = matcher.pattern_compare(user_input)
response = matcher.response_compare(user_input, intent_class)

generated_response = matcher.ResponseGenerator(response)

print(response)

print(generated_response)
