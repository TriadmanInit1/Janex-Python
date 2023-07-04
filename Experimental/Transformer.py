import numpy as np

# Define the Transformer components

class PositionalEncoding:
    def __init__(self, d_model, max_seq_len):
        self.d_model = d_model
        self.max_seq_len = max_seq_len

    def get_positional_encoding(self, positions):
        angles = np.arange(self.d_model) / self.d_model
        angles = angles[np.newaxis, :]  # Shape: (1, d_model)

        positions = positions[:, np.newaxis]  # Shape: (max_seq_len, 1)
        angles = angles * (1 / np.power(10000, 2 * positions / self.d_model))
        angles[:, 0::2] = np.sin(angles[:, 0::2])
        angles[:, 1::2] = np.cos(angles[:, 1::2])

        return angles  # Shape: (max_seq_len, d_model)

class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_head = d_model // num_heads

        self.W_q = np.random.randn(d_model, d_model)
        self.W_k = np.random.randn(d_model, d_model)
        self.W_v = np.random.randn(d_model, d_model)
        self.W_o = np.random.randn(d_model, d_model)

    def attention(self, Q, K, V):
        scores = np.matmul(Q, K.T) / np.sqrt(self.d_head)  # Shape: (num_heads, seq_len, seq_len)
        attention_weights = softmax(scores, axis=-1)  # Apply softmax along the last axis

        attended_values = np.matmul(attention_weights, V)  # Shape: (num_heads, seq_len, d_head)
        return attended_values

    def forward(self, X):
        Q = np.matmul(X, self.W_q)
        K = np.matmul(X, self.W_k)
        V = np.matmul(X, self.W_v)

        Q_split = np.split(Q, self.num_heads, axis=-1)
        K_split = np.split(K, self.num_heads, axis=-1)
        V_split = np.split(V, self.num_heads, axis=-1)

        attended_values = []
        for i in range(self.num_heads):
            attended_values.append(self.attention(Q_split[i], K_split[i], V_split[i]))

        concatenated = np.concatenate(attended_values, axis=-1)  # Shape: (seq_len, d_model)
        output = np.matmul(concatenated, self.W_o)

        return output

class FeedForwardNetwork:
    def __init__(self, d_model, d_ff):
        self.d_model = d_model
        self.d_ff = d_ff

        self.W_1 = np.random.randn(d_model, d_ff)
        self.W_2 = np.random.randn(d_ff, d_model)

    def forward(self, X):
        hidden = np.matmul(X, self.W_1)
        hidden = np.maximum(hidden, 0)  # Apply ReLU activation
        output = np.matmul(hidden, self.W_2)

        return output

# Create a simple Transformer model

def softmax(x, axis=-1):
    # Apply softmax operation to the input array along the specified axis
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e_x / np.sum(e_x, axis=axis, keepdims=True)

class Transformer:
    def __init__(self, d_model, num_heads, d_ff, num_layers):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_ff = d_ff
        self.num_layers = num_layers

        self.layers = []
        for _ in range(num_layers):
            self.layers.append(
                (MultiHeadAttention(d_model, num_heads), FeedForwardNetwork(d_model, d_ff))
            )

    def forward(self, X):
        for _ in range(self.num_layers):
            attention_output = self.layers[_][0].forward(X)
            X = X + attention_output  # Residual connection
            X = X + self.layers[_][1].forward(X)  # Residual connection

        return X

# Example usage

max_seq_len = 10
d_model = 64
num_heads = 4
d_ff = 128
num_layers = 2

pos_enc = PositionalEncoding(d_model, max_seq_len)
X = np.random.randn(max_seq_len, d_model)  # Input sequence
positions = np.arange(max_seq_len)
pos_encoding = pos_enc.get_positional_encoding(positions)

X_with_pos_enc = X + pos_encoding

transformer = Transformer(d_model, num_heads, d_ff, num_layers)
output = transformer.forward(X_with_pos_enc)

import numpy as np

# Define the necessary classes and functions (same as the code provided)

# Example usage
max_seq_len = 10
d_model = 64
num_heads = 4
d_ff = 128
num_layers = 2

# Tokenize the sentence
sentence = "You are an alien."
tokens = sentence.split()  # Split by whitespace
num_tokens = len(tokens)

# Encode the tokens
token_to_id = {"You": 1, "are": 2, "an": 3, "alien": 4}  # Remove the period from 'alien'
encoded_tokens = [token_to_id[token] for token in tokens]

# Pad or truncate the sequence
if num_tokens < max_seq_len:
    padded_tokens = encoded_tokens + [0] * (max_seq_len - num_tokens)
else:
    padded_tokens = encoded_tokens[:max_seq_len]

# Convert the numerical sequence into a NumPy array
X = np.array(padded_tokens)

# Apply positional encoding
pos_enc = PositionalEncoding(d_model, max_seq_len)
positions = np.arange(max_seq_len)
pos_encoding = pos_enc.get_positional_encoding(positions)

# Add positional encodings to the input
X_with_pos_enc = X + pos_encoding

# Create a Transformer model
transformer = Transformer(d_model, num_heads, d_ff, num_layers)

# Process the input through the Transformer model
output = transformer.forward(X_with_pos_enc)

# Print the output
print(output)
