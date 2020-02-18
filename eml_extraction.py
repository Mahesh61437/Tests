import os
import re

path = './'
files_listing = os.listdir(path)

list_contents = ['Message-ID', 'From', 'To', 'Date', 'Cc', 'Subject']

final_list = []
final_list.append(list_contents)

email_regex = r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)'
for file in files_listing:
    if str.lower(file[-3:]) == "eml":
        message_id = ''
        from_mail = ''
        to_mail = ''
        date = ''
        cc = ''
        with open(file, 'r') as eml_file:
            raw = eml_file.readlines()
            for i in raw:

                for word in list_contents:
                    if i.startswith(word):
                        if word == 'Message-ID':
                            message_id = i[13:-2]
                        elif word == 'From':
                            from_mail = re.findall(email_regex, i, re.M | re.I)[0]
                        elif word == 'To':
                            to_mail = re.findall(email_regex, i, re.M | re.I)[0]

                        elif word == 'Date':
                            date = i.strip()[6:22].strip()
                        elif word == 'Cc':
                            cc = i[4:-1]

        with open(file, 'r') as eml_file:
            contents = eml_file.read()
            raw_contents = repr(contents)
            if raw_contents.split('Subject:')[1].split(":")[0][-2:] == 'Re':
                string = raw_contents.split('Subject:')[1].split(":")[1]
                second_string = string.split("\\n")[0]
                subject = "Re: " + second_string.strip()
            elif raw_contents.split('Subject:')[1].split(":")[0][-2:] == 'To':
                subject = raw_contents.split('Subject:')[1].split(":")[0][:-4].strip()
            elif raw_contents.split('Subject:')[1].split(":")[0][-4:] == 'From':
                subject = raw_contents.split('Subject:')[1].split(":")[0][:-6].strip()

        final_list.append([message_id, from_mail, to_mail, date, cc, subject])

mx = len(max((sub[0] for sub in final_list), key=len))
for row in final_list:
    print(" ".join(["{:<{mx}}".format(ele, mx=mx) for ele in row]))
