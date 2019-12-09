import csv
from lxml import html
from os import listdir
from os.path import isfile, join

def trip_reports_to_csv():
    # the csv file we're writing reports to
    trip_csv = "trips.csv"
    # the values we're extracting from each report
    columns = ["report", "title", "substance"]
    # the directory we have our report html files in
    mypath = "experiences"
    # grab string names of only files from dir defined above
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

    # open 'trips.csv' for writing
    with open(trip_csv, "w") as trip_csv:
        trip_writer = csv.writer(trip_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write row with column names
        trip_writer.writerow(columns)
        # for every file in `experiences` directory
        for f in onlyfiles:
            with open(f, "r", encoding='utf-8', errors='ignore') as f_:
                try:
                    page = f_.read()
                    tree = html.fromstring(page)
                    # get report text by joining all text values inside the div that surrounds it
                    report = ''.join(tree.xpath('//div[@class="report-text-surround"]/text()')).strip()
                    # grab title of trip report
                    title = tree.xpath('//div[@class="title"]/text()')[0]
                    # grab the substance that motivates this report
                    substance = tree.xpath('//div[@class="substance"]/text()')[0]
                    # write data to a new row
                    trip_writer.writerow([report, title, substance])
                except:
                    # if something failed in the above block (broken html, missing element) just skip the error and pass along
                    pass

# call the method that does everything
trip_reports_to_csv()
