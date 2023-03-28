import Utilities
import os

path_for_folder = "/home/eugene/Рабочий стол"
file_name = "FileForLab"
full_path = os.path.join(path_for_folder, file_name)

# file_lines = [line for line in open(full_path, encoding="UTF8")]
# f = open(full_path, encoding="UTF8")
# tmp = f.read();
# print(tmp)

if(Utilities.check_file(full_path)):
    f = open(full_path, encoding="UTF8")
    tmp = f.read();
    print(Utilities.total_number_sentences(tmp))
    print(Utilities.count_nondeclarative_sentences(tmp))
    print(Utilities.average_len_words(tmp))
    print(Utilities.average_len_sentences(tmp))
    print(Utilities.top_repeted_grams(tmp))




