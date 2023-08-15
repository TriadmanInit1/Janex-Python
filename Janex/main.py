import json
import random
import os
import string
from Cipher import *

class IntentMatcher:
    def __init__(self, intents_file_path, thesaurus_file_path):
        self.intents_file_path = intents_file_path
        self.intents = self.train()
        self.thesaurus_file_path = thesaurus_file_path
        self.sentenceconstructors = [
            "also", "moreover", "besides", "however", "nevertheless", "thus", "therefore", "meanwhile", "furthermore",
            "nonetheless", "likewise", "similarly", "otherwise", "instead", "consequently", "hence", "otherwise", "because",
            "since", "although", "though", "unless", "until", "when", "while", "whereas", "inasmuch", "after", "before", "if",
            "then", "lest", "provided", "once", "whenever", "wherever", "notwithstanding", "hitherto", "nowadays", "henceforth"
            "meanwhile", "thereupon", "whereupon", "notably", "indeed", "further", "more", "too", "very", "quite", "almost",
            "entirely", "just", "simply", "nearly", "actually", "truly", "really", "certainly", "well", "just", "almost",
            "perhaps", "maybe", "probably", "possibly", "certainly", "definitely", "undoubtedly", "clearly", "obviously",
            "honestly", "seriously", "basically", "essentially", "specifically", "particularly", "practically", "literally",
            "generally", "typically", "currently", "recently", "previously", "originally", "officially", "apparently", "finally",
            "subsequently", "immediately", "gradually", "significantly", "considerably", "respectively", "similarly",
            "notably", "likewise", "comparatively", "overall", "therefore", "consequently", "accordingly", "meanwhile"
            ]


    def tokenize(self, input_string):
        new_string = ""

        deletion = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        input_string = input_string.lower()

        for x in input_string:
            if x not in deletion:
                new_string += x

        processed_string = new_string
        words = processed_string.split(" ")

        return words

    def tokenize_list(self, input_list):
        token_words = []
        for word in input_list:
            token = self.tokenize(word)
            token_words.append(token)

        return token_words

    def train(self):
        try:
            with open(self.intents_file_path, "r") as file:
                intents = json.load(file)
        except:
            print(f"Janex: '{self.intents_file_path}' file does not appear to exist in your program's directory. Downloading default template, courtesy of SoapDoesCode...")
            os.system(f"curl -o {self.intents_file_path} https://raw.githubusercontent.com/Cipher58/intents-file/main/intents.json")
            with open(self.intents_file_path, "r") as file:
                intents = json.load(file)
        return intents

    def pattern_compare(self, input_string):
        highest_similarity = 0
        most_similar_pattern = None
        similarity_percentage = 0
        letters_full = self.letter_splitter(input_string)

        for intent_class in self.intents["intents"]:
            overall_word_list = []
            similarity = 0
            word_list = []

            for pattern in intent_class["patterns"]:
                pattern_lower = str(pattern)
                pattern_lower = pattern_lower.lower()
                word_list = self.tokenize(pattern_lower)
                overall_word_list.append(word_list)
                new_list = []
                new_bag = []

                for word in word_list:
                    word = self.stem(word)
                    new_list.append(word)

                word_list_2 = self.tokenize(input_string)
                for word in word_list_2:
                    word = self.stem(word)
                    new_bag.append(word)

                word_list = new_list
                word_list_2 = new_bag

                for word in word_list_2:
                    if word in word_list:
                        if word.lower() in self.sentenceconstructors:
                            length = self.measure_letters(word)
                            similarity += length
                        else:
                            length = self.measure_letters(word)
                            similarity =+ length*2

                if similarity > highest_similarity:
                    similarity_percentage = similarity / (len(overall_word_list) + len(word_list_2))
                    highest_similarity = similarity
                    most_similar_pattern = pattern
                    most_similar_class = intent_class

#        print(f"Similarity: {similarity_percentage:.2%}")

        if most_similar_pattern:
            highest_similarity = highest_similarity / 100
            return most_similar_class, highest_similarity
        else:
            highest_similarity = 0
            for intent_class in self.intents["intents"]:
                similarity = 0
                for pattern in intent_class["patterns"]:
                    input_chars = self.letter_splitter(input_string)
                    output_chars = self.letter_splitter(pattern)
                    for a in input_chars:
                        if a in output_chars:
                            similarity =+ 1
                            if similarity > highest_similarity:
                                similarity_percentage = similarity / (len(overall_word_list) + len(word_list_2))
                                most_similar_pattern = pattern
                                highest_similarity = similarity
                                most_similar_class = intent_class

            return most_similar_class, highest_similarity

    def response_compare(self, input_string, intent_class):
        highest_similarity = 0
        similarity_percentage = 0
        distance = 0
        most_similar_response = None

        responses = intent_class["responses"] if intent_class else []

        for response in responses:
            if response:
                similarity = 0
                Count = 0
                InputCount = 0

                response_lower = response.lower()
                word_list = self.tokenize(response_lower)
                new_list = []
                new_bag = []

                for word in word_list:
                    word = self.stem(word)
                    new_list.append(word)

                word_list_2 = self.tokenize(input_string)
                for word in word_list_2:
                    word = self.stem(word)
                    new_bag.append(word)

                word_list = new_list
                word_list_2 = new_bag
                overall_word_list = word_list + word_list_2

                for word in word_list_2:
                    if word in word_list:
                        length = self.measure_letters(word)
                        # Check if the word begins with a capital letter
                        if word.istitle():
                            similarity += length*3
                        elif word.lower() in self.sentenceconstructors:
                            similarity += length  # Add 2 to the similarity for words with capital letters
                        else:
                            similarity += length*2

                response_words = self.tokenize(response)
                input_words = self.tokenize(input_string)

                for word in response_words:
                    Count += self.measure_letters(word)

                for word in input_words:
                    InputCount += self.measure_letters(word)

                distance = Count + InputCount / 2

                if Count > InputCount:
                    distance = Count - InputCount
                else:
                    distance = InputCount - Count

                similarity_percentage = similarity / len(overall_word_list)  # Calculate average similarity

                if similarity > highest_similarity:
                    highest_similarity = similarity
                    most_similar_response = response


                if most_similar_response:
                    return most_similar_response
                else:
                    highest_similarity = 0
                    responses = []
                    randoresponses = []

                    for response in intent_class["responses"]:
                        responses.append(response)

                    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                        choice = random.choice(responses)
                        randoresponses.append(choice)

                    most_similar_response = random.choice(randoresponses)

                    return most_similar_response

    def stem(self, input_word):
        suffixes = ["ing", "ly", "ed", "es", "'s", "er", "est", "y", "ily", "able", "ful", "ness", "less", "ment", "ive", "ize", "ous"]
        for suffix in suffixes:
            if input_word.endswith(suffix):
                input_word = input_word[:-len(suffix)]
                break
        return input_word

    def stem_sentence(self, input_string):
        word_list = input_string.split(" ")
        stemmed_words = []

        for input_word in word_list:
            word = self.stem(input_word)
            stemmed_word.append(word)

        return stemmed_words

    def stem_list(self, input_list):
        stemmed_words = []
        for word in input_list:
            stemmed_word = self.stem(word)
            stemmed_words.append(stemmed_word)

        return stemmed_words

    # Experimental Development Zone

    def SynonymCompare(self, word):
        thesaurus = self.load_thesaurus()
        for synonym in thesaurus[word]["synonyms"]:
            random_newword = random.choice(thesaurus[word]["synonyms"])

        return random_newword

    def legacy_generate_sentence(self, words):
        sentence = ' '.join(words)
#        sentence = sentence.capitalize()
        if sentence[-1] not in '.!?':
            sentence =+ random.choice('.!?')
        return sentence

    def LegacyResponseGenerator(self, most_similar_response):
        new_sentence = []
        deletion = string.punctuation
        most_similar_response_splitted = most_similar_response.split()
        self.thesaurus = self.load_thesaurus()
        for word in most_similar_response_splitted:
            if word in self.thesaurus:
                synonyms = self.thesaurus[word]["synonyms"]
                new_word = random.choice(synonyms)
                new_sentence.append(new_word)
            else:
                new_sentence.append(word)

        generated_response = self.generate_sentence(new_sentence)

        initial_response = []

        for i in most_similar_response:
            initial_response.append(i)

        return generated_response


    def ResponseGenerator(self, most_similar_response):

        deletion = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        punctuation = self.template(most_similar_response)

        thesaurus = self.load_thesaurus()

        thes_words = self.extract_titles()

        most_similar_response_splitted = []

        most_similar_response_splitted = most_similar_response.split(" ")

        for word in thes_words:
            syns = thesaurus[word]["synonyms"]
            for syn in syns:
                for element in most_similar_response_splitted:
                    syn = str(syn)
                    element = str(element)
                    for x in deletion:
                        if x in syn:
                            syn = syn.replace(x, "")
                        if x in element:
                            element = element.replace(x, "")
                    if syn.lower() == element.lower():
                        new_word = random.choice(syns)
                        for x in deletion:
                            if element.endswith(x):
                                new_word = f"{new_word}{x}"
                        if element.istitle():
                            new_word = new_word[:1].upper() + new_word[1:]
                        most_similar_response = most_similar_response.replace(element, new_word)

        generated_response = most_similar_response

        return generated_response

    def template(self, input_string):

        newtemplate = []
        deletion = '''!()-[]{};:'"\,<>./?@#$%^&*_~ '''

        for x in input_string:
            if x not in deletion:
                newtemplate += "╔"
            elif x in deletion:
                newtemplate += x

#        print(newtemplate)

        return newtemplate

    def load_thesaurus(self):
        try:
            with open(self.thesaurus_file_path, "r") as f:
                thesaurus = json.load(f)
        except:

            print(f"Janex: '{self.thesaurus_file_path}' file does not appear to exist in your program's directory. Downloading default template...")
            self.download_thesaurus()

            with open(self.thesaurus_file_path, "r") as f:
                thesaurus = json.load(f)

        return thesaurus

    def update_thesaurus(self):
        try:
            os.remove(f"{self.thesaurus_file_path}")
        except:
            print(f"Janex: '{self.thesaurus_file_path}' file does not appear to exist in your program's directory. Skipping deletion...")

        self.download_thesaurus()

        with open(self.thesaurus_file_path, "r") as f:
            thesaurus = json.load(f)

        return thesaurus

    def download_thesaurus(self):
        os.system(f"curl -o {self.thesaurus_file_path} https://raw.githubusercontent.com/Cipher58/intents-file/main/thesaurus.json")

    def measure_letters(self, input_string):
        return sum(char.isalpha() for char in input_string)

    def read_class_titles(self):
        with open(f"{self.thesaurus_file_path}", "r") as file:
            data = json.load(file)
        class_titles = list(data.keys())
        return class_titles

    def extract_titles(self):
        titlelist = []
        class_titles = self.read_class_titles()
        for title in class_titles:
            titlelist.append(title)

        return titlelist

    def letter_splitter(self, input_text):
        letters_in_order = []
        for char in input_text:
            letters_in_order.append(char)

#        print(letters_in_order)

        return letters_in_order
