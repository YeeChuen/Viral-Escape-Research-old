# Author/s: Yee Chuen Teh
# Title: readcsv.py
# Project: ChowdhuryLab Datamining from website
# Description: python scripts to read creating csv file. 
#               aim to check/reference the created PBD_SequenceDF.csv

#____________________________________________________________________________________________________
# imports 
import csv
import argparse
import sys
import os.path

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
                    line_count += 1
                elif str(row[1]) == str(search):
                    print(f'\t ROW: {row[0]} | PBDID: {row[1]} | PBD INFO: {row[2]}\n \t--> PBD Sequence: {row[3]}.')
                    found = True
                    line_count += 1
        print("\n")
        if search != None:
            if found == False:
                print("No results for PBDID: {}".format(search))
            else:
                print("Search for PBDID: {}".format(search))
        else:
            print("Result for all PBDID")
        print("Total PBD count: {}".format(str(line_count-1)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fPath', type=str, required=True)
    parser.add_argument('--search', type=str, required=False)
    fPath = "--fPath"
    if fPath not in sys.argv[1:]:
        print("To use \"readcsv.py\", please specify which csv file to read.\n")
        print("REQUIRED: Type \"readcsv.py --fPath <filename.csv>\", to read the specific csv file.")
        print("Replace <filename.csv> with a csv file to be read.\n")
        print("OPTIONAL: Type \"readcsv.py --fPath <filename.csv> --search <PBDID no.>\", to read the specific PBD in the given csv file.")
        print("Replace <PBDID no.> with a PBDID to be search.")
        return
    args = parser.parse_args()
    csvfile = args.fPath
    if not os.path.exists(csvfile):
        print("Unable to locate file \"{}\", make sure specified csv file exists.".format(csvfile))
        return
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
