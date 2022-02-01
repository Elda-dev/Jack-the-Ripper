import csv
import ripper

def downloadcsv(input_csv):
    csvlist = []
    with open(input_csv, newline='', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            csvlist.append(row)
        for row in csvlist:
            if row[4] != "Album" and row[0] != "Track name":
                try:
                    ripper.DownloadMusic(row[0] + " by " + row[1], './Output', row[0], row[1], row[2])
                except:
                    continue
                print(row[0] + " Has been downloaded")

csv_path = input("csv file name:")
downloadcsv(csv_path)