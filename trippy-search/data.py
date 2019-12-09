import csv
from lxml import html
from os import listdir
from os.path import isfile, join

def trip_reports_to_csv():
    trip_csv = "trips.csv"
    columns = ["report", "title", "substance"]
    mypath = "experiences"
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

    with open(trip_csv, "w") as trip_csv:
        trip_writer = csv.writer(trip_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        trip_writer.writerow(columns)
        for f in onlyfiles:
            with open(f, "r", encoding='utf-8', errors='ignore') as f_:
                try:
                    page = f_.read()
                    tree = html.fromstring(page)
                    report = ''.join(tree.xpath('//div[@class="report-text-surround"]/text()')).strip()
                    title = tree.xpath('//div[@class="title"]/text()')[0]
                    substance = tree.xpath('//div[@class="substance"]/text()')[0]
                    trip_writer.writerow([report, title, substance])
                except:
                    pass

trip_reports_to_csv()
