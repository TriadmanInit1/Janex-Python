import numpy as np

def string_vectorize(input_string):
    ascii_values = [ord(char) for char in input_string]  # Get ASCII values for each character
    ascii_vectors = np.array(ascii_values)              # Convert the list to a numpy array
    return ascii_vectors

def reshape_array_dimensions(array, dimensions):
    target_dim = dimensions
    vector1 = np.resize(array, target_dim)
    return vector1

def calculate_cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)

    if norm_vector1 == 0 or norm_vector2 == 0:
        return 0  # Handle zero division case

    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity

if __name__ == "__main__":
    firststring = input("First string: ")
    firstvectors = string_to_ascii_vectors(firststring)

    secondstring = input("Second string: ")
    secondvectors = string_to_ascii_vectors(secondstring)

    print(f"First string vectors: {firstvectors}")
    print(f"Second string vectors: {secondvectors}")

    print("Calculating cosine similarity.")

    dimensions = int(input("Dimensions: "))

    firstvectors = reshape_array_dimensions(firstvectors, dimensions)
    secondvectors = reshape_array_dimensions(secondvectors, dimensions)

    print(f"Reshaped to {dimensions} dimensions: {firstvectors}")
    print(f"Reshaped to {dimensions} dimensions: {secondvectors}")

    similarity = calculate_cosine_similarity(firstvectors, secondvectors)

    print(f"Similarity: {similarity}")
