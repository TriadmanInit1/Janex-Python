from main import *

intents_file_path = "./intents.json"
matcher = IntentMatcher(intents_file_path)

input_string = input("You: ")

intent_class, percentage = matcher.pattern_compare(input_string)
response = matcher.response_compare(input_string, intent_class)

#try:
generated_response = matcher.ResponseGenerator(response)
#except:
#    pass

print(response)

#try:
print(generated_response)
#except:
#    pass
