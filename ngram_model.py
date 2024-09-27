import os
import re
from nltk import ngrams, FreqDist
from collections import Counter


def extract_java_methods(file_path):
    """
    Extracts all methods from a Java file and returns a list of methods.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Improved regular expression to match various Java method definitions, including multi-line method signatures.
    # method_pattern = re.compile(
    #     r'(public|private|protected|static|final|abstract|synchronized|native|strictfp)\s+[\w$<>\[\]]+\s+\w+\s*\([^)]*\)',
    #     re.MULTILINE
    # )

    # method_pattern = re.compile(
    #     r'''
    #     (?P<modifiers>(?:(?:public|private|protected|static|final|abstract|synchronized|native|strictfp)\s+)+)  # Match one or more modifiers
    #     (?P<return_type>[\w$<>\[\]]+\s+)  # Match return type
    #     (?P<method_name>\w+)  # Match method name
    #     \s*  # Optional whitespace
    #     \((?P<parameters>[^)]*)\)  # Match parameter list
    #     ''',
    #     re.VERBOSE
    # )
    # method_pattern = re.compile(r'''
    #     (public\s+static\s+class\s+Effects\s+\{\s*    # Match the beginning of the Effects class
    #     (?:                                           # Start non-capturing group
    #         \s*                                       # Possible whitespace
    #         public\s+static\s+final\s+String\s+       # Match public static final String
    #         [A-Z_][A-Z0-9_]*\s*=\s*                   # Match variable name and equals sign
    #         "[^"]*";\s*                               # Match string literal and semicolon
    #     )*                                            # Repeat zero or more times
    #     \s*                                           # Possible whitespace
    #     \})                                           # Match the end of the Effects class
    # ''', re.VERBOSE)
    # content = method_pattern.findall(content)
    return content


def generate_ngrams(text, n):
    words = text.split()
    ngrams = [' '.join(words[i:i + n]) for i in range(len(words) - n + 1)]
    return ngrams


def analyze_ngrams(text, n=2):
    ngrams = generate_ngrams(text, n)
    freq_counts = Counter(ngrams)
    return freq_counts


def collect_all_methods(root_dir):
    """
    Recursively extract all methods from Java files in the specified root directory.
    """
    all_methods = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(subdir, file)
                methods = extract_java_methods(file_path)
                text = analyze_ngrams(methods, n=6)
                all_methods.extend(text)
    print(f"Extracted {len(all_methods)} methods.")
    print("Preprocessing methods...")
    print("Building N-gram model...")
    all_methods = Counter(all_methods)
    most_common_1000 = all_methods.most_common(2000)
    show_ng = most_common_1000[790:800]
    print(f"Top 10 n-grams: {show_ng}")
    print("Displaying part of the N-gram model...")
    for ngram, freq in show_ng:
        print(f"{[ngram]} : {freq}")
    exit()
    return all_methods


def preprocess_methods(methods):
    """
    Preprocess the list of methods by removing comments, empty lines, and irrelevant information.
    """
    cleaned_methods = []
    for method in methods:
        # Remove comments and empty lines
        method = re.sub(r'//.*|/\*[\s\S]*?\*/', '', method)  # Remove single-line and multi-line comments
        method = re.sub(r'\s+', ' ', method).strip()  # Remove excess whitespace
        cleaned_methods.append(method)
    return cleaned_methods


def build_ngram_model(tokens, N):
    """
    Build an N-gram model and return the frequency distribution of N-grams.
    """
    ngrams_list = list(ngrams(tokens, N))
    ngram_freq = FreqDist(ngrams_list)
    return ngram_freq


def tokenize_method(method):
    """
    Split the method into tokens and return a list of tokens.
    """
    # Use regular expressions for tokenization, a simple approach suitable for most Java code
    tokens = re.findall(r'\b\w+\b', method)
    # tokens = method.split()

    return tokens


# def is_valid_java_dir(path):
#     """
#     Determines if the path is a valid directory containing Java files (excluding non-source directories).
#     """
#     exclude_dirs = ['docs', 'gradle', 'SPD-classes', 'build', 'bin', 'out', 'test']
#     return not any(excluded in path for excluded in exclude_dirs)

def is_valid_java_dir(path):
    """
    Determines if the given path is not in the excluded non-source directories.
    """
    exclude_dirs = ['docs', 'gradle', 'SPD-classes', 'build', 'bin', 'out', 'test']
    # Construct a complete list of excluded paths based on the parent directory of the current path
    parent_dir = os.path.dirname(path)
    excluded_paths = [os.path.join(parent_dir, excluded) for excluded in exclude_dirs]
    # Check if the given path starts with any of the excluded paths
    return not any(path.startswith(excluded) for excluded in excluded_paths)


def main():
    # Project root directory
    project_root = 'core/src/main/java/com/shatteredpixel/shatteredpixeldungeon'  # Use relative path to recursively traverse the entire project

    # Step 1: Extract all methods
    print("Extracting Java methods...")
    all_methods = []
    for subdir, _, _ in os.walk(project_root):
        if is_valid_java_dir(subdir):
            methods = collect_all_methods(subdir)
            all_methods.extend(methods)

    print(f"Extracted {len(all_methods)} methods.")
    cleaned_methods = []
    # Step 2: Preprocess methods
    print("Preprocessing methods...")
    for methods in all_methods:
        cleaned = preprocess_methods(methods)
        cleaned_methods.append(cleaned)

    # Step 3: Build N-gram model
    print("Building N-gram model...")
    all_tokens = []
    for method in cleaned_methods:
        tokens = tokenize_method(method)
        all_tokens.extend(tokens)

    # Build a trigram model
    n = 3
    ngram_model = build_ngram_model(all_tokens, n)
    print(f"Top 10 n-grams: {ngram_model.most_common(10)}")

    # Step 4: Display part of the N-gram model
    print("Displaying part of the N-gram model...")
    for ngram, freq in ngram_model.most_common(10):
        print(f"{ngram} : {freq}")


if __name__ == '__main__':
    main()
