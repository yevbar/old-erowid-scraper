import csv

with open('trips.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if "The Return to Oz" in row:
            print("We found it")
            print(row)
