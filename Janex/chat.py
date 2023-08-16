from main import *

intents_file_path = "./intents.json"
thesaurus_file_path = "./thesaurus.json"

matcher = IntentMatcher(intents_file_path, thesaurus_file_path)

input_string = input("You: ")

encodedinput = matcher.encode_string_to_numbers(input_string)

print(encodedinput)

intent_class, percentage = matcher.pattern_compare(input_string)
response = matcher.response_compare(input_string, intent_class)

#try:
generated_response = matcher.ResponseGenerator(response)
#except:
#    pass

print(response)

#try:
print(generated_response)

encodedresponse = matcher.encode_string_to_numbers(generated_response)

print(encodedresponse)

print("")

completedcode = encodedinput + encodedresponse

completedoutput = matcher.decode_numbers_to_string(completedcode)
#except:
#    pass

print("")
print("")

print(completedoutput)
