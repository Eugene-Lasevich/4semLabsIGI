import re
import collections

list_of_single_abbreviations = ["etc.", "vs.", "Jr.", "Sr.", "Dr.", "Smth.", "Smb.", "Mr.", "Mrs."]
list_of_double_abbreviations = ["e.g.", "i.e.", "a.m.", "p.m.", "P.S."]
list_of_triple_abbreviations = ["V.I.P.", "M.V.P.", "P.S.S."]


def check_file(path: str):
    file_lines = [line for line in open(path, encoding="UTF8")]
    incorect_lines = []
    flag = True
    for line in file_lines:
        if (re.findall(r'[А-я]', line)):
            incorect_lines.append(line)
            flag = False
    if (flag == False):
        print("These sentences contain invalid characters")
        for line in incorect_lines:
            print(line)

    return flag


def __count_abbreviations(text: str):
    counter = 0
    for el in list_of_single_abbreviations:
        counter += text.count(el)
    for el in list_of_double_abbreviations:
        counter += text.count(el) * 2
    for el in list_of_triple_abbreviations:
        counter += text.count(el) * 3

    return counter


def total_number_sentences(text: str):
    result = re.findall(r"(\.+|\!+\?+|\?+\!+|\?+|\!+)", text)
    return len(result) - __count_abbreviations(text)


def count_nondeclarative_sentences(text: str):
    result = re.findall('\!+\?+|\?+\!+|\?+|\!+', text)
    return len(result)


def __list_of_words(text: str):
    words = re.findall(r'\b\w+\b', text)
    nums = re.findall(r'\b\d+\b', text)
    list_words = [word for word in words if word not in nums]
    return list_words


def average_len_words(text: str):
    total_lenght = 0
    total_words = __list_of_words(text)

    for word in total_words:
        total_lenght += len(word)

    return total_lenght / len(total_words)


def average_len_sentences(text: str):
    total_lenght = 0
    total_words = __list_of_words(text)

    for word in total_words:
        total_lenght += len(word)

    return  total_lenght/total_number_sentences(text)




def top_repeted_grams(text: str, k: int = 4, n: int = 4):
    words = re.findall(r'\b\w+\b', text)
    ngrams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    top_ngrams = collections.Counter(ngrams).most_common(k)
    return top_ngrams
