import os
import re
from nltk import ngrams, FreqDist
from collections import Counter


def extract_java_methods(file_path):
    """
    从Java文件中提取所有方法的内容，返回方法的列表。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 改进的正则表达式，匹配各种Java方法的定义，包括多行方法签名
    # method_pattern = re.compile(
    #     r'(public|private|protected|static|final|abstract|synchronized|native|strictfp)\s+[\w$<>\[\]]+\s+\w+\s*\([^)]*\)',
    #     re.MULTILINE
    # )

    # method_pattern = re.compile(
    #     r'''
    #     (?P<modifiers>(?:(?:public|private|protected|static|final|abstract|synchronized|native|strictfp)\s+)+)  # 匹配一个或多个修饰符
    #     (?P<return_type>[\w$<>\[\]]+\s+)  # 匹配返回类型
    #     (?P<method_name>\w+)  # 匹配方法名
    #     \s*  # 可选空白
    #     \((?P<parameters>[^)]*)\)  # 匹配参数列表
    #     ''',
    #     re.VERBOSE
    # )
    # method_pattern = re.compile(r'''
    #     (public\s+static\s+class\s+Effects\s+\{\s*    # 匹配 Effects 类的开始
    #     (?:                                           # 开始非捕获组
    #         \s*                                       # 可能的空格
    #         public\s+static\s+final\s+String\s+       # 匹配 public static final String
    #         [A-Z_][A-Z0-9_]*\s*=\s*                   # 匹配变量名和等号
    #         "[^"]*";\s*                               # 匹配字符串字面量和分号
    #     )*                                            # 重复零次或多次
    #     \s*                                           # 可能的空格
    #     \})                                           # 匹配 Effects 类的结束
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
    从指定的根目录中递归提取所有Java文件中的方法。
    """
    all_methods = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(subdir, file)
                methods = extract_java_methods(file_path)
                text = analyze_ngrams(methods, n=6)
                all_methods.extend(text)
    print(f"共提取了 {len(all_methods)} 个方法。")
    print("预处理方法...")
    cleaned_methods = preprocess_methods(all_methods)
    print("构建N-gram模型...")
    all_tokens = []
    for method in cleaned_methods:
        tokens = tokenize_method(method)
        all_tokens.extend(tokens)
    all_methods = Counter(all_methods)
    most_common_1000 = all_methods.most_common(2000)
    show_ng = most_common_1000[790:800]
    print(f"Top 10 n-grams: {show_ng}")
    print("展示部分N-gram模型...")
    for ngram, freq in show_ng:
        print(f"{[ngram]} : {freq}")
    exit()
    return all_methods


def preprocess_methods(methods):
    """
    对方法列表进行预处理，去除注释、空行等无关信息。
    """
    cleaned_methods = []
    for method in methods:
        # 去除注释和空行
        method = re.sub(r'//.*|/\*[\s\S]*?\*/', '', method)  # 去除单行和多行注释
        method = re.sub(r'\s+', ' ', method).strip()  # 去除多余空白字符
        cleaned_methods.append(method)
    return cleaned_methods


def build_ngram_model(tokens, N):
    """
    构建N-gram模型，返回ngram频率分布。
    """
    ngrams_list = list(ngrams(tokens, N))
    ngram_freq = FreqDist(ngrams_list)
    return ngram_freq


def tokenize_method(method):
    """
    将方法拆分为标记（tokens），返回一个标记列表。
    """
    # 使用正则表达式进行分词，简单处理，适用于大多数Java代码
    tokens = re.findall(r'\b\w+\b', method)
    # tokens = method.split()

    return tokens


# def is_valid_java_dir(path):
#     """
#     判断是否为包含Java文件的有效目录（排除非源码目录）
#     """
#     exclude_dirs = ['docs', 'gradle', 'SPD-classes', 'build', 'bin', 'out', 'test']
#     return not any(excluded in path for excluded in exclude_dirs)

def is_valid_java_dir(path):
    """
    判断给定的路径是否不包含在非源码目录中
    """
    exclude_dirs = ['docs', 'gradle', 'SPD-classes', 'build', 'bin', 'out', 'test']
    # 构造一个完整的排除路径列表，以当前路径的父目录为基准
    parent_dir = os.path.dirname(path)
    excluded_paths = [os.path.join(parent_dir, excluded) for excluded in exclude_dirs]
    # 检查给定路径是否以任何一个排除路径为前缀
    return not any(path.startswith(excluded) for excluded in excluded_paths)


def main():
    # 项目根目录
    project_root = 'core/src/main/java/com/shatteredpixel/shatteredpixeldungeon'  # 使用相对路径来递归整个项目

    # 第一步：提取所有方法
    print("提取Java方法...")
    all_methods = []
    for subdir, _, _ in os.walk(project_root):
        if is_valid_java_dir(subdir):
            methods = collect_all_methods(subdir)
            all_methods.extend(methods)

    print(f"共提取了 {len(all_methods)} 个方法。")
    cleaned_methods = []
    # 第二步：预处理
    print("预处理方法...")
    for methods in all_methods:
        cleaned = preprocess_methods(methods)
        cleaned_methods.append(cleaned)

    # 第三步：构建N-gram模型
    print("构建N-gram模型...")
    all_tokens = []
    for method in cleaned_methods:
        tokens = tokenize_method(method)
        all_tokens.extend(tokens)

    # 构建三元模型
    n = 3
    ngram_model = build_ngram_model(all_tokens, n)
    print(f"Top 10 n-grams: {ngram_model.most_common(10)}")

    # 第四步：示例展示
    print("展示部分N-gram模型...")
    for ngram, freq in ngram_model.most_common(10):
        print(f"{ngram} : {freq}")


if __name__ == '__main__':
    main()
