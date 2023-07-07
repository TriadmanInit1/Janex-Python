const readline = require("readline");

class IntentMatcher {
  constructor(intentsFilePath) {
    this.intentsFilePath = intentsFilePath;
    this.intents = this.train();
  }

  Tokenize(inputString) {
    let processedString = inputString.toLowerCase().trim().replace(/[^\w\s]|_/g, "").replace(/\s+/g, " ");
    let words = processedString.split(" ");

    words = this.stemList(words);

    return words;
  }

  TokenizeList(inputList) {
    let tokenWords = [];
    for (let word of inputList) {
      let token = this.Tokenize(word);
      tokenWords.push(token);
    }

    return tokenWords;
  }

  train() {
    const fs = require("fs");
    const intents = JSON.parse(fs.readFileSync(this.intentsFilePath, "utf8"));
    return intents;
  }

  patternCompare(inputString) {
    let inputStringLower = inputString.toLowerCase();
    let highestSimilarity = 0;
    let mostSimilarPattern = null;
    let similarityPercentage = 0;

    for (let intentClass of this.intents.intents) {
      let overallWordList = [];
      let similarity = 0;

      for (let pattern of intentClass.patterns) {
        let wordList = [];
        let patternLower = pattern.toLowerCase();
        wordList = this.Tokenize(patternLower);
        overallWordList.push(wordList);
        let newList = [];
        let newBag = [];

        for (let word of wordList) {
          word = this.stem(word);
          newList.push(word);
        }

        let wordList2 = this.Tokenize(inputStringLower);
        for (let word of wordList2) {
          word = this.stem(word);
          newBag.push(word);
        }

        wordList = newList;
        wordList2 = newBag;

        for (let word of wordList2) {
          if (wordList.includes(word)) {
            similarity++;
          }
        }

        if (similarity > highestSimilarity) {
          similarityPercentage = similarity / (overallWordList.length + wordList2.length);
          highestSimilarity = similarity;
          mostSimilarPattern = intentClass;
        }
      }
    }

    console.log(`Similarity: ${similarityPercentage.toFixed(2)}%`);

    if (mostSimilarPattern) {
      return mostSimilarPattern;
    } else {
      throw new Error("No matching intent class found.");
    }
  }

  responseCompare(inputString, intentClass) {
    let inputStringLower = inputString.toLowerCase();
    let highestSimilarity = 0;
    let similarityPercentage = 0;
    let mostSimilarResponse = null;

    let responses = intentClass ? intentClass.responses : [];

    for (let response of responses) {
      let similarity = 0;
      let responseLower = response.toLowerCase();
      let wordList = this.Tokenize(responseLower);
      let newList = [];
      let newBag = [];

      for (let word of wordList) {
        word = this.stem(word);
        newList.push(word);
      }

      let wordList2 = this.Tokenize(inputStringLower);
      for (let word of wordList2) {
        word = this.stem(word);
        newBag.push(word);
      }

      wordList = newList;
      wordList2 = newBag;

      for (let word of wordList2) {
        if (wordList.includes(word)) {
          similarity += 1 / (wordList.length + wordList2.length);
        }
      }

      if (similarity > highestSimilarity) {
        similarityPercentage = similarity * 100;
        highestSimilarity = similarity;
        mostSimilarResponse = response;
      }
    }

    console.log(`Similarity: ${similarityPercentage.toFixed(2)}%`);

    // Convert mostSimilarResponse back into the original string
    for (let response of responses) {
      let lowResponseList = [];
      let lowResponse = response.toLowerCase();
      lowResponseList = this.stemSentence(lowResponse);

      for (let lowResponseWord of lowResponseList) {
        if (lowResponseWord === mostSimilarResponse) {
          mostSimilarResponse = response;
        }
      }
    }

    return mostSimilarResponse;
  }

  stem(inputWord) {
    let suffixes = ["ing", "ly", "ed", "es", "'s", "er", "est", "y", "ily", "able", "ful", "ness", "less", "ment", "ive", "ize", "ous"];
    for (let suffix of suffixes) {
      if (inputWord.endsWith(suffix)) {
        inputWord = inputWord.slice(0, -suffix.length);
        break;
      }
    }
    return inputWord;
  }

  stemSentence(inputString) {
    let wordList = [];
    let stemmedWords = [];
    wordList = inputString.split(" ");
    for (let inputWord of wordList) {
      let word = this.stem(inputWord);
      stemmedWords.push(word);
    }

    return stemmedWords;
  }

  stemList(inputList) {
    let stemmedWords = [];
    for (let word of inputList) {
      let stemmedWord = this.stem(word);
      stemmedWords.push(stemmedWord);
    }

    return stemmedWords;
  }

  outputCompare(output) {
    let highestSimilarity = 0;
    let mostSimilarPattern = null;
    let similarityPercentage = 0;

    for (let intentClass of this.intents.intents) {
      let overallWordList = [];
      let similarity = 0;

      for (let pattern of intentClass.patterns) {
        let wordList = [];
        let patternLower = pattern.toLowerCase();
        wordList = this.Transform(patternLower);
        overallWordList.push(wordList);
        let newList = [];
        let newBag = [];

        for (let word of wordList) {
          newList.push(word);
        }

        let wordList2 = output;
        for (let word of wordList2) {
          newBag.push(word);
        }

        wordList = newList;
        wordList2 = newBag;

        for (let word of wordList2) {
          if (wordList.includes(word)) {
            similarity++;
          }
        }

        if (similarity > highestSimilarity) {
          similarityPercentage = similarity / (overallWordList.length + wordList2.length);
          highestSimilarity = similarity;
          mostSimilarPattern = intentClass;
        }
      }
    }

    console.log(`Similarity: ${similarityPercentage.toFixed(2)}%`);

    if (mostSimilarPattern) {
      return mostSimilarPattern;
    } else {
      throw new Error("No matching intent class found.");
    }
  }
}

// Example usage:
const intentsFilePath = "./intents.json";
const matcher = new IntentMatcher(intentsFilePath);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question("You: ", (input) => {
  // Use the input here
  console.log("User input:", input);

  // Close the readline interface
  rl.close();

  const intentClass = matcher.patternCompare(input);
  const response = matcher.responseCompare(input, intentClass);
  console.log(response);
});
