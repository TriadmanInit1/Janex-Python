import json
import random
import os

class IntentMatcher:
    def __init__(self, intents_file_path):
        self.intents_file_path = intents_file_path
        self.intents = self.train()

    def tokenize(self, input_string):
        processed_string = input_string.lower().strip().replace(r"[^\w\s]|_", "").replace(r"\s+", " ")
        words = processed_string.split(" ")

        return words

    def tokenize_list(self, input_list):
        token_words = []
        for word in input_list:
            token = self.tokenize(word)
            token_words.append(token)

        return token_words

    def train(self):
        with open(self.intents_file_path, "r") as file:
            intents = json.load(file)
        return intents

    def pattern_compare(self, input_string):
        input_string_lower = input_string.lower()
        highest_similarity = 0
        most_similar_pattern = None
        similarity_percentage = 0

        for intent_class in self.intents["intents"]:
            overall_word_list = []
            similarity = 0

            for pattern in intent_class["patterns"]:
                word_list = []
                pattern_lower = pattern.lower()
                word_list = self.tokenize(pattern_lower)
                overall_word_list.append(word_list)
                new_list = []
                new_bag = []

                for word in word_list:
                    word = self.stem(word)
                    new_list.append(word)

                word_list_2 = self.tokenize(input_string_lower)
                for word in word_list_2:
                    word = self.stem(word)
                    new_bag.append(word)

                word_list = new_list
                word_list_2 = new_bag

                for word in word_list_2:
                    if word in word_list:
                        similarity += 1

                if similarity > highest_similarity:
                    similarity_percentage = similarity / (len(overall_word_list) + len(word_list_2))
                    highest_similarity = similarity
                    most_similar_pattern = intent_class

#        print(f"Similarity: {similarity_percentage:.2%}")

        if most_similar_pattern:
            highest_similarity = highest_similarity / 100
            return most_similar_pattern, highest_similarity
        else:
            raise ValueError("No matching intent class found.")

    def response_compare(self, input_string, intent_class):
        input_string_lower = input_string.lower()
        highest_similarity = 0
        similarity_percentage = 0
        distance = 0
        most_similar_response = None

        responses = intent_class["responses"] if intent_class else []

        for response in responses:
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

            word_list_2 = self.tokenize(input_string_lower)
            for word in word_list_2:
                word = self.stem(word)
                new_bag.append(word)

            word_list = new_list
            word_list_2 = new_bag
            overall_word_list = word_list + word_list_2

            for word in word_list_2:
                if word in word_list:
            # Check if the word begins with a capital letter
                    if word.istitle():
                        similarity += 2  # Add 2 to the similarity for words with capital letters
                    else:
                        similarity += 1

            response_words = self.tokenize(response)
            input_words = self.tokenize(input_string)

            for word in response_words:
                Count += 0.01

            for word in input_words:
                InputCount += 0.01

            distance = Count + InputCount / 2

#            print(distance)

            similarity = similarity - distance

        # Calculate the similarity percentage and the distance
            similarity_percentage = similarity / len(overall_word_list)  # Calculate average similarity

            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_response = response

#        print(f"Similarity: {similarity_percentage:.2%}")
#        print(f"Distance: {distance}")

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
        newword = None
        thesaurus = self.load_thesaurus()
        for synonym in thesaurus[word]["synonyms"]:
            for associate in thesaurus[word]["related"]:
                if synonym in associate:
                    newword = associate

        if newword is not None:
            return newword
        else:
            random_newword = random.choice(thesaurus[word]["related"])
            return random_newword

    def ResponseGenerator(self, most_similar_response):
        thesaurus = self.load_thesaurus()

        tokens = self.tokenize(most_similar_response)

        for i, token in enumerate(tokens):
            for word in thesaurus:
                if token == thesaurus[word]["synonyms"]:
                    newword = self.SynonymCompare(word)
                    tokens[i] = newword

        generated_response = " ".join(tokens)

        return generated_response

    def load_thesaurus(self):
        file_path = "thesaurus.json"
        try:
            with open(file_path, "r") as f:
                thesaurus = json.load(f)
        except:
            thesaurus = {
              "happy": {
                "synonyms": ["joyful", "content", "pleased", "ecstatic", "elated", "happy"],
                "related": ["cheerful", "delighted", "satisfied", "blissful", "jubilant"]
              },
              "sad": {
                "synonyms": ["unhappy", "miserable", "depressed", "heartbroken", "gloomy"],
                "related": ["melancholy", "dismal", "downhearted", "despondent", "despairing"]
              },
              "beautiful": {
                "synonyms": ["gorgeous", "stunning", "lovely", "attractive", "charming"],
                "related": ["elegant", "mesmerizing", "exquisite", "enchanting", "radiant"]
              },
              "angry": {
                "synonyms": ["furious", "irate", "outraged", "indignant", "incensed"],
                "related": ["enraged", "fuming", "infuriated", "livid", "exasperated"]
              },
              "brave": {
                "synonyms": ["courageous", "fearless", "valiant", "heroic", "daring"],
                "related": ["bold", "gallant", "fear-defying", "intrepid", "valorous"]
              },
              "fast": {
                "synonyms": ["quick", "speedy", "rapid", "swift", "expeditious"],
                "related": ["hasty", "fleet", "brisk", "accelerated", "nimble"]
              },
              "small": {
                "synonyms": ["tiny", "little", "miniature", "minute", "compact"],
                "related": ["petite", "diminutive", "microscopic", "undersized", "wee"]
              },
              "big": {
                "synonyms": ["large", "huge", "enormous", "gigantic", "massive"],
                "related": ["immense", "colossal", "vast", "monumental", "tremendous"]
              },
              "good": {
                "synonyms": ["excellent", "superb", "wonderful", "terrific", "fantastic", "good"],
                "related": ["great", "awesome", "outstanding", "amazing", "splendid", "wonderful"]
              },
              "bad": {
                "synonyms": ["terrible", "horrible", "awful", "dreadful", "atrocious"],
                "related": ["abysmal", "appalling", "disastrous", "lousy", "woeful"]
              },
              "smart": {
                "synonyms": ["intelligent", "clever", "wise", "bright", "brilliant"],
                "related": ["knowledgeable", "astute", "sharp", "savvy", "perceptive"]
              },
              "funny": {
                "synonyms": ["humorous", "amusing", "comical", "hilarious", "witty"],
                "related": ["entertaining", "jovial", "jocular", "lighthearted", "mirthful"]
              },
              "difficult": {
                "synonyms": ["challenging", "hard", "complicated", "complex", "tricky"],
                "related": ["demanding", "arduous", "strenuous", "problematic", "daunting"]
              },
              "more": {
                "synonyms": ["more", "extra", "else"],
                "related": ["further", "furthermore", "extra", "even more", "additional"]
              },
              "say": {
                "synonyms": ["say", "speaks"],
                "related": ["state", "say", "assert"]
              },
              "strong": {
                "synonyms": ["powerful", "robust", "sturdy", "mighty", "potent"],
                "related": ["forceful", "vigorous", "resilient", "unyielding", "indomitable"]
              },
              "kind": {
                "synonyms": ["compassionate", "benevolent", "generous", "considerate", "thoughtful"],
                "related": ["gentle", "sympathetic", "empathetic", "caring", "tender"]
              },
              "cold": {
                "synonyms": ["chilly", "freezing", "frigid", "icy", "frosty"],
                "related": ["cool", "numb", "polar", "subzero", "wintry"]
              },
              "hot": {
                "synonyms": ["sweltering", "scorching", "sizzling", "boiling", "burning"],
                "related": ["sultry", "torrid", "blistering", "fiery", "heated"]
              },
              "tired": {
                "synonyms": ["exhausted", "weary", "fatigued", "drained", "spent"],
                "related": ["drowsy", "sleepy", "worn-out", "enervated", "frazzled"]
              },
              "calm": {
                "synonyms": ["serene", "tranquil", "peaceful", "composed", "placid"],
                "related": ["relaxed", "untroubled", "undisturbed", "soothing", "mellow"]
              },
              "happy": {
                "synonyms": ["joyful", "content", "pleased", "ecstatic", "elated", "happy"],
                "related": ["cheerful", "delighted", "satisfied", "blissful", "jubilant"]
              },
              "afraid": {
                "synonyms": ["scared", "frightened", "terrified", "nervous", "anxious"],
                "related": ["apprehensive", "panicked", "worried", "fearful", "jittery"]
              },
              "honest": {
                "synonyms": ["truthful", "sincere", "upright", "genuine", "honorable"],
                "related": ["trustworthy", "faithful", "reliable", "scrupulous", "loyal"]
              },
              "bright": {
                "synonyms": ["luminous", "radiant", "brilliant", "shining", "gleaming"],
                "related": ["vivid", "glowing", "dazzling", "beaming", "glittering"]
              },
              "shy": {
                "synonyms": ["bashful", "timid", "reserved", "reticent", "introverted"],
                "related": ["modest", "coy", "nervous", "hesitant", "self-effacing"]
              },
              "sick": {
                "synonyms": ["ill", "unwell", "ailing", "infirmed", "under the weather"],
                "related": ["weak", "queasy", "indisposed", "vomiting", "feverish"]
              },
              "quiet": {
                "synonyms": ["silent", "peaceful", "serene", "hushed", "muted"],
                "related": ["tranquil", "calm", "noiseless", "still", "muffled"]
              },
              "excited": {
                "synonyms": ["thrilled", "enthusiastic", "eager", "animated", "jubilant"],
                "related": ["ecstatic", "elated", "rapturous", "exhilarated", "passionate"]
              },
              "tasty": {
                "synonyms": ["delicious", "savory", "appetizing", "delectable", "yummy"],
                "related": ["flavorful", "palatable", "scrumptious", "mouthwatering", "tantalizing"]
              },
              "beautiful": {
                "synonyms": ["gorgeous", "stunning", "lovely", "attractive", "charming"],
                "related": ["elegant", "mesmerizing", "exquisite", "enchanting", "radiant"]
              },
              "angry": {
                "synonyms": ["furious", "irate", "outraged", "indignant", "incensed"],
                "related": ["enraged", "fuming", "infuriated", "livid", "exasperated"]
              },
              "vast": {
                "synonyms": ["enormous", "immense", "boundless", "expansive", "limitless"],
                "related": ["gigantic", "colossal", "massive", "huge", "tremendous"]
              },
              "loud": {
                "synonyms": ["noisy", "boisterous", "cacophonous", "blaring", "deafening"],
                "related": ["clamorous", "raucous", "thunderous", "uproarious", "piercing"]
              },
              "happy": {
                "synonyms": ["joyful", "content", "pleased", "ecstatic", "elated", "happy"],
                "related": ["cheerful", "delighted", "satisfied", "blissful", "jubilant"]
              },
              "sad": {
                "synonyms": ["unhappy", "miserable", "depressed", "heartbroken", "gloomy"],
                "related": ["melancholy", "dismal", "downhearted", "despondent", "despairing"]
              },
              "hot": {
                "synonyms": ["sweltering", "scorching", "sizzling", "boiling", "burning"],
                "related": ["sultry", "torrid", "blistering", "fiery", "heated"]
              },
              "bright": {
                "synonyms": ["luminous", "radiant", "brilliant", "shining", "gleaming"],
                "related": ["vivid", "glowing", "dazzling", "beaming", "glittering"]
              },
              "strange": {
                "synonyms": ["unusual", "peculiar", "odd", "bizarre", "weird"],
                "related": ["curious", "abnormal", "mysterious", "eccentric", "quirky"]
              },
              "empty": {
                "synonyms": ["vacant", "void", "bare", "deserted", "unoccupied"],
                "related": ["hollow", "barren", "desolate", "devoid", "blank"]
              },
              "calm": {
                "synonyms": ["serene", "tranquil", "peaceful", "composed", "placid"],
                "related": ["relaxed", "untroubled", "undisturbed", "soothing", "mellow"]
              },
              "cold": {
                "synonyms": ["chilly", "freezing", "frigid", "icy", "frosty"],
                "related": ["cool", "numb", "polar", "subzero", "wintry"]
              },
              "long": {
                "synonyms": ["lengthy", "extended", "prolonged", "endless", "never-ending"],
                "related": ["long-lasting", "lingering", "continual", "interminable", "eternal"]
              },
              "short": {
                "synonyms": ["brief", "concise", "succinct", "compact", "abrupt"],
                "related": ["quick", "fleeting", "transient", "momentary", "ephemeral"]
              },
              "tall": {
                "synonyms": ["high", "towering", "elevated", "lofty", "giant"],
                "related": ["statuesque", "sky-scraping", "majestic", "colossal", "immense"]
              },
              "wet": {
                "synonyms": ["damp", "moist", "drenched", "soggy", "soaked"],
                "related": ["humid", "watery", "drizzly", "sopping", "saturated"]
              },
              "dry": {
                "synonyms": ["arid", "parched", "thirsty", "barren", "dehydrated"],
                "related": ["bone-dry", "deserted", "waterless", "sterile", "drought-stricken"]
              },
              "rich": {
                "synonyms": ["wealthy", "affluent", "prosperous", "opulent", "well-to-do"],
                "related": ["abundant", "plentiful", "loaded", "well-off", "moneyed"]
              },
              "poor": {
                "synonyms": ["impoverished", "destitute", "needy", "indigent", "deprived"],
                "related": ["penurious", "broke", "bankrupt", "struggling", "impecunious"]
              },
              "old": {
                "synonyms": ["elderly", "aged", "mature", "vintage", "senior"],
                "related": ["ancient", "antique", "time-worn", "hoary", "time-honored"]
              },
              "new": {
                "synonyms": ["fresh", "novel", "innovative", "modern", "contemporary"],
                "related": ["recent", "current", "up-to-date", "unfamiliar", "state-of-the-art"]
              },
              "old-fashioned": {
                "synonyms": ["outdated", "antiquated", "obsolete", "vintage", "archaic"],
                "related": ["retro", "dated", "bygone", "old-school", "nostalgic"]
              },
              "modern": {
                "synonyms": ["contemporary", "up-to-date", "current", "innovative", "progressive", "modern"],
                "related": ["advanced", "futuristic", "trendy", "cutting-edge", "state-of-the-art"]
              },
              "brilliant": {
                "synonyms": ["dazzling", "radiant", "shining", "glittering", "glowing", "brilliant"],
                "related": ["sparkling", "vivid", "resplendent", "luminous", "effulgent"]
              },
              "stupid": {
                "synonyms": ["foolish", "idiotic", "dim-witted", "dense", "dull"],
                "related": ["dumb", "silly", "brain-dead", "ignorant", "imbecilic"]
              },
              "simple": {
                "synonyms": ["easy", "uncomplicated", "straightforward", "plain", "basic"],
                "related": ["elementary", "effortless", "undemanding", "uninvolved", "uncomplicated"]
              },
              "complex": {
                "synonyms": ["complicated", "intricate", "involved", "elaborate", "multi-faceted"],
                "related": ["difficult", "convoluted", "intricate", "perplexing", "challenging"]
              },
              "expensive": {
                "synonyms": ["costly", "pricey", "high-priced", "lavish", "valuable"],
                "related": ["luxurious", "premium", "extravagant", "exorbitant", "sumptuous"]
              },
              "cheap": {
                "synonyms": ["inexpensive", "affordable", "low-cost", "economical", "bargain"],
                "related": ["budget-friendly", "reasonable", "thrifty", "cost-effective", "economy"]
              },
              "dangerous": {
                "synonyms": ["hazardous", "risky", "perilous", "treacherous", "unsafe"],
                "related": ["life-threatening", "unsafe", "precarious", "life-endangering", "reckless"]
              },
              "safe": {
                "synonyms": ["secure", "protected", "harmless", "unhurt", "untouched"],
                "related": ["out of danger", "secure", "shielded", "guarded", "unscathed"]
              },
              "assist": {
                "synonyms": ["help", "aid", "support", "aid", "abet"],
                "related": ["facilitate", "aid", "serve", "contribute", "back"]
              }
            }
            with open(file_path, "w") as f:
                json.dump(thesaurus, f)
        return thesaurus
