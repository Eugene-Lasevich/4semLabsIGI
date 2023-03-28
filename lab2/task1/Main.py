import Utilities
import os

path_for_folder = "/home/eugene/Рабочий стол"
file_name = "FileForLab"
full_path = os.path.join(path_for_folder, file_name)


if(Utilities.check_file(full_path)):
    file = open(full_path, encoding="UTF8")
    text = file.read();
    print(f"Total number of sentences {Utilities.total_number_sentences(text)}")
    print(f"Total number of non declarative sentences {Utilities.count_nondeclarative_sentences(text)}")
    print(f"Average length words {Utilities.average_len_words(text)}")
    print(f"Average length sentensec {Utilities.average_len_sentences(text)}")
    print(f"Top-k N-grams{Utilities.top_repeted_grams(text)}")




