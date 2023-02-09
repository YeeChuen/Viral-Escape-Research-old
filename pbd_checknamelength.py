# Author/s: Yee Chuen Teh
# Title: TODO: script name
# Project: TODO: project title
# Description: TODO: Description
# Reference:
'''
TODO: write your reference here
Usage: 
python pbd_checknamelength.py --f PoreDB_old/PoreDB.fas
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
from pbd_length import *
#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def extract_name(fas_list):
    '''fas_list is a list where even index is description, odd index is sequence'''
    name_list = []
    for i in range(0,len(fas_list), 2):
        description = fas_list[i]
        n_list = description.split("|")
        name = n_list[0]
        truename = name.replace(">","")
        name_list.append(truename)
    return name_list

def check_namelength(name_list):
    dict = {}
    max_freq = 0
    maxfreq_length = 0
    max_length = 0

    for s in name_list:
        length = len(s)
        max_length = max(length, max_length)
        if length in dict:
            dict[length]+=1
        else:
            dict[length] = 1
        if dict[length] >max_freq:
            max_freq = dict[length]
            maxfreq_length = length

    myKeys = list(dict.keys())
    myKeys.sort()
    sorted_key = {i: dict[i] for i in myKeys}

    for k in sorted_key:
        print("Frequency of protein with name length {}: {}".format(str(k), str(dict[k])))

    print("Highest protein frequence with name length {}: {}".format(str(maxfreq_length), str(max_freq)))
    print("total number of protein in selected file: {}".format(str(len(name_list))))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, required=True) 
    args = parser.parse_args()
    path = args.f
    a_temp = fas_to_list(path)
    b_temp = extract_name(a_temp)
    check_namelength(b_temp)

    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<PYTHON SCRIPT TITLE>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<PYTHON SCRIPT TITLE>\" script --------------------\n")