from intentclassifier import *
import random

Classifier = IntentClassifier()

Classifier.set_intentsfp("intents.json")
Classifier.set_vectorsfp("vectors.json")
Classifier.set_dimensions(300)

Classifier.train_vectors()

Input = input("You: ")

classification = Classifier.classify(Input)

response = random.choice(classification["responses"])

print(response)
