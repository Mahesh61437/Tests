import os

path = './'
files_listing = os.listdir(path)

for file in files_listing:
    total_words = set()
    if str.lower(file[-3:]) == "txt":
        file_path = os.path.join(path) + file
        print("file name : ", file_path)
        with open(file_path, 'r') as txt_file:
            contents = txt_file.readlines()
            lines = len(contents)
            print("number of lines: ",lines)
            line_count=0
            for line in contents:
                lower_string_set = line.lower().split(" ")
                line_count += 1
                words = line.split(' ')
                word_set = set(words)
                total_words = set(lower_string_set) | total_words
                print("number of unique words in line ", line_count, ": ", len(set(lower_string_set)))
                print("unique words in line ", line_count, ": ", list(word_set))

            print("total unique words in file : ", list(set(total_words)))
