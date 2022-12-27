# Author/s: Yee Chuen Teh
# Title: readcsv.py
# Project: ChowdhuryLab Datamining from website
# Description: python scripts to read creating csv file. 
#               aim to check/reference the created PBDSequenceDF.csv

#____________________________________________________________________________________________________
# imports 
import csv
import argparse

#____________________________________________________________________________________________________
# functions 

def printcsv(csvfile, search = None):
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        found = False
        for row in csv_reader:
            if line_count == 0:
                print(f'\tColumns: {", ".join(row)}')
                line_count += 1
            else:
                if search == None:
                    print(f'\t ROW: {row[0]}. PBDID: {row[1]} | PBD INFO: {row[2]}\n \t--> PBD Sequence: {row[3]}.')
                elif str(row[1]) == str(search):
                    print(f'\t ROW: {row[0]}. PBDID: {row[1]} | PBD INFO: {row[2]}\n \t--> PBD Sequence: {row[3]}.')
                line_count += 1
        print("\n")
        if search != None:
            if found == False:
                print("unable to search for PBDID {}".format(search))
            else:
                print("search for PBDID {}".format(search))
        print("Total PBD count: {}".format(str(line_count)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fPath', type=str, required=True)
    parser.add_argument('--search', type=str, required=False)
    args = parser.parse_args()
    csvfile = args.fPath
    if args.search:
        search = str(args.search)   
        printcsv(csvfile, search)
    else:
        printcsv(csvfile)

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__": 
    print("\n-------------------- START of \"readcsv.py\" script --------------------")
    main()
    print("-------------------- END of \"readcsv.py\" script --------------------\n")
