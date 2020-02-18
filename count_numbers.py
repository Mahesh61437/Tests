import os
import re

path = './'
files_listing = os.listdir(path)

only_percentages_regex = r'([-+]?\d*\.\d+%|\d+%)'
only_dollar_regex = r'\$(\d+)'
only_amount_regex = r'Amount(\s+\d+)'
all_matching_regex = r'([-+]?\d*\.\d+%|\d+%|\d*\.\d+|\d+)'

for file in files_listing:
    if str.lower(file[-3:]) == "txt":
        print("file name : ", file)
        with open(file, 'r') as txt_file:

            raw_contents = repr(txt_file.read())

            percentages = re.findall(only_percentages_regex, raw_contents)
            print("all percentages == ",percentages)

            dollars = re.findall(only_dollar_regex, raw_contents)
            print("all dollars amounts == ",dollars)

            amounts = re.findall(only_amount_regex, raw_contents)
            print("all amounts with prefix 'Amount'",amounts)

            percentages_symbol_count = len(percentages)
            amount_count = len(dollars) + len(amounts)

            only_amounts = dollars + amounts

            all_matches = re.findall(all_matching_regex, raw_contents)

            print("percentage symbol count == ", percentages_symbol_count)
            print("Amount count == ", amount_count)
            print("All percentages == ", percentages)
            print("All amounts starting with 'Amount' and '$' ==== ", only_amounts, "\n\n")

            all_amount_matches = []
            for num in all_matches:
                if '%' not in num:
                    only_amounts.append(num)
            print("All amounts without '%' symbol ==== ", only_amounts, "\n\n")


