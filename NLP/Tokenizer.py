import string

def Tokenize(input_string):
    input_string = input_string.strip()
    
    input_string = input_string.translate(str.maketrans("", "", string.punctuation))
    
    words = input_string.split()
    
    return words

input_string = input("You: ")

output = Tokenize(input_string)

print(output)
