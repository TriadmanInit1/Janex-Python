const readline = require("readline");
const IntentMatcher = require("./Janex.js");

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
