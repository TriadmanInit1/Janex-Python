def tokenize_text(text):
    return text.split()  # Split the text into words

def encode_words(words, word_to_number):
    encoded_words = []

    for word in words:
        encoded_words.append(word_to_number[word])

    return encoded_words

def generate_occurrence_matrix(encoded_words):
    matrix = [[0] * len(word_to_number) for _ in range(len(word_to_number))]

    for i in range(1, len(encoded_words)):
        prev_word = encoded_words[i - 1]
        current_word = encoded_words[i]
        matrix[prev_word][current_word] += 1

    return matrix

def generate_compressed_string(encoded_words, matrix):
    compressed_string = []

    for i in range(1, len(encoded_words)):
        prev_word = encoded_words[i - 1]
        current_word = encoded_words[i]
        compressed_string.append(str(matrix[prev_word][current_word]) + ":" + str(current_word))

    return " ".join(compressed_string)

def decode_compressed_string(compressed_string, word_to_number):
    decoded_words = []
    compressed_parts = compressed_string.split()

    for part in compressed_parts:
        count, code = part.split(":")
        count = int(count)
        code = int(code)

        word = list(word_to_number.keys())[list(word_to_number.values()).index(code)]
        decoded_words.append(word * count)

    return " ".join(decoded_words)

# Example usage
input_texts = [
    "hello world hello",
    "world hello world",
    "this is a test",
    "your mum is gay",
    "your dad sells avon",
    "your nan eats toes",
    "the quick brown fox jumps over the lazy dog"
]

input_string = input("You: ")

all_words = []

# Existing code...

# Tokenize all input texts
for text in input_texts:
    words = tokenize_text(text)
    all_words.extend(words)

# Convert all words to lowercase
all_words = [word.lower() for word in all_words]

# Create a mapping and encode all words
unique_words = list(set(all_words))
word_to_number = {word: i for i, word in enumerate(unique_words)}
encoded_words = []

for text in input_texts:
    words = tokenize_text(text)
    encoded_words.extend(encode_words(words, word_to_number))

# Generate occurrence matrix
matrix = generate_occurrence_matrix(encoded_words)

# Compress
compressed_string = generate_compressed_string(encoded_words, matrix)

print("Input Texts:", input_texts)
print("Compressed String:", compressed_string)

print("")

decoded_string = decode_compressed_string(compressed_string, word_to_number)

print("Translated: ", decoded_string)

character_list = [char for char in input_string]

encoded_input_string = encode_words(character_list, word_to_number)

combined_encoded_words = []
# Combine encoded_input_string and encoded_words
combined_encoded_words = encoded_input_string + encoded_words

# Generate occurrence matrix for combined encoded words
combined_matrix = generate_occurrence_matrix(combined_encoded_words)

# Compress the combined encoded words
compressed_combined_string = generate_compressed_string(combined_encoded_words, combined_matrix)

print("Input Texts:", input_texts)
print("Compressed Combined String:", compressed_combined_string)

print("")

# Decode the compressed combined string
decoded_combined_string = decode_compressed_string(compressed_combined_string, word_to_number)

print("Decoded Combined String:", decoded_combined_string)
