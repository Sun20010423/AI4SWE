# Java Method Extraction and N-gram Model Analysis

## Introduction
In this project, I have developed a script to extract Java method definitions from a source code corpus and build an N-gram model to analyze the structural patterns of these methods. The N-gram model helps in identifying common code patterns and structures, which can be useful for tasks like code completion and style analysis.

## Requirements
To run this project, I have used the following software and libraries:
- **Python 3.x**: Required for executing the script.
- **Required Python Libraries**:
  - `nltk` for natural language processing.
  - `re` for regular expression operations.
  - `collections` for handling frequency distributions.

You can install the necessary libraries using the following command:

```bash
pip install nltk
```

## Configuration and Execution

### 1. Clone the Repository

### 2. Configure the Dataset

### 3. Running the Script

Navigate to the root directory of the project and execute the script using the following command:

python ngram_model.py

The script performs the following tasks:

1. Extracts Java methods from the source files.
2. Preprocesses the extracted methods by removing comments and whitespace.
3. Tokenizes the methods and builds an N-gram model.
4. Displays the top 10 most common N-grams.

### 4. Sample Corpus

I have included a sample corpus in the `core/src/main/java/com/shatteredpixel/shatteredpixeldungeon` directory. You can replace the existing files or add more Java files to this directory if you wish to use your own corpus.

### 5. Output

The script outputs the top 10 most common N-grams along with their frequencies. This output helps in understanding the most frequently used patterns and structures in the analyzed Java methods.

