# Janex
A free open-source framework which can be used to build Machine Learning tools, LLMs, and Natural Language Processing scripts with full simplicity.

<h2> What is the purpose of Janex? </h2>

Monopolistic companies are confining their Artificial Intelligence research to themselves, and capitalising on it. Even companies that swore to open source their software (OpenAI) went back on their morals, with the releases of GPT-3+, as did other powerful businesses.

These businesses go on to sell their research to the Government, and sell access to it to the public. As such, my aim is to create a framework that you can use to easily construct your own language models, and other machine learning algorithms, as I believe this power should not be held firmly in the hands of corrupt rich politicians and advantaged capitalists. (It will take a while before it reaches a practical level)

Released under the **new** Free Lily License 1.0, Janex will improve and become a useful tool for users to conduct their own research in the potential of Artifical Intelligence.

<h3> How to use </h3>

<h5> Adding to your project </h5>

Firstly, you'll need to install the library using the Python pip package manager.

```
python3 -m pip install Janex

```
Secondly, you need to import the library into your Python script.

```
from Janex import *
```

<h4>Using Janex in your code</h4>

<h5>Create an instance</h5>

Before anything else, you need to create an instance of the IntentMatcher class.

```
intents_file_path = "./intents.json"

matcher = IntentMatcher(intents_file_path)
```

<h5>Tokenizing:</h5>

To utilise the tokenizer feature, here is an example of how it can be used.

```
input_string = "Hello! What is your name?"

words = matcher.Tokenize(input_string)

print(words)
```

<h5>Intent classifying:</h5>

To compare the input with the patterns from your intents.json storage file, you have to declare the intents file path.

```
intents_file_path = "intents.json"

intent_class = matcher.pattern_compare(input_string, intents_file_path)

print(intent_class)
```

<h5>Response similarity:</h5>

Sometimes a list of responses in a class can become varied in terms of context, and so in order to get the best possible response, we can use the 'responsecompare' function to compare the input string with your list of responses.

```
BestResponse = matcher.response_compare(input_string, intents_file_path, intent_class)

print(BestResponse)
```

<h5>Using Transformers:</h5>

I am still currently learning about complex mathematical Machine Learning algorithms, so the numpy-based transformers included in this project are still in development, and may not always be useful or stable for a while. If you would like to use them for whatever, here's an example.

```
output = matcher.Transform(input_string)
print(output)
```

<h3> Functionality </h3>

<h4>Version 0.0.5</h4>

- Word tokenizer ✓
- Intent classifier ✓
- Word Stemmer ✓
- Support for Darwin, Unix-like and Windows ✓
- Simple text transformer ✓
