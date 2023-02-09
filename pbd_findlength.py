# Author/s: Yee Chuen Teh
# Title: pbd_findlength.py (update as of 2/8/2023)
# Project: Chowdhury Lab Viral Escape
# Description: this script serve to find protein of a given specific length
# Reference:
'''
TODO: write your reference here
Usage:
python pbd_findlength.py --f PoreDB_nonRNA/Muscle_3W5B_1 --l 1398
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
import argparse
import os
import sys
from pbd_length import *

#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def get_from_length(fas_list, target_length):
    a_temp = []
    for i in range(0, len(fas_list),2):
        if len(fas_list[i+1]) == target_length:
            a_temp.append(fas_list[i])
    
    return a_temp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, required=True)     # file location
    parser.add_argument('--l', type=int, required=True)     # the target length, specify what length to report, 
                                                            # can check length from "pbd_length.py"
    args = parser.parse_args()
    a_temp = fas_to_list(args.f)
    b_temp = get_from_length(a_temp, args.l)
    print("Protein ID that are of length {}".format(str(args.l)))
    for n in b_temp:
        print(n[1:7])
    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<pbd_findlength.py>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<pbd_findlength.py>\" script --------------------\n")