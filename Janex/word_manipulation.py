def tokenize(input_string):
    input_string = str(input_string)

    new_string = ""
    deletion = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    input_string = input_string.lower()

    for x in input_string:
        if x not in deletion:
            new_string += x

    words = []

    processed_string = new_string
    words = processed_string.split(" ")

    return words

def stem(input_word):
    suffixes = ["ing", "ly", "ed", "es", "'s", "er", "est", "y", "ily", "able", "ful", "ness", "less", "ment", "ive", "ize", "ous"]
    for suffix in suffixes:
        if input_word.endswith(suffix):
            input_word = input_word[:-len(suffix)]
            break
    return input_word
