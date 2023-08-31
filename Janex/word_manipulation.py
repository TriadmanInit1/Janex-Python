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
