
BagOfWords = []

def Tokenize(input_string):
    Words = input_string.split()
    BagOfWords.append(Words)
    return BagOfWords

input_string = input("You: ")

Output = Tokenize(input_string)

print(Output)
