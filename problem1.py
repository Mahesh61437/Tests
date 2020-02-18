"""

change the path to the path of your file
and run the file with command : python3 problem1.py

I wrote this code in mac.So i'm not sure how it will work with windows or any other OS.
In case you are using Windows or any other OS, please try to analyze my code.

"""

import csv

path = './interview_scent.csv'


# reading the given CSV file
with open(path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    count = 0
    none_count = 0
    predictions_list = []
    predictions_dict = {}

    for row in csv_reader:
        #checking if predictions column is None
        if row[4] == 'None':
            none_count += 1
        elif row[4] != 'predictions':
            # if predictions is not None,
            # add it into a dictionary and increment the value every time the same key appears
            count += 1
            if row[4] in predictions_dict:
                predictions_dict[row[4]] = predictions_dict[row[4]] + 1
            else:
                predictions_dict[row[4]] = 1

print("total number of rows, where predictions is not NONE === ", count)
print("total number of rows, where predictions is  NONE === ", none_count)
print("distinct values of predictions === ", [*predictions_dict])

# writing the output to a CSV file
with open("./output.csv", 'w') as csv_file:
    fieldnames = ['Predictions', 'PredictionCount']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for prediction, prediction_count in predictions_dict.items():
        writer.writerow({'Predictions': prediction, 'PredictionCount': prediction_count})
