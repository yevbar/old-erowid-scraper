import csv

with open('trips.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count += 1
        if line_count in [270, 271, 272]:
            print(row)
    print("There are lotsa lines:", line_count)
