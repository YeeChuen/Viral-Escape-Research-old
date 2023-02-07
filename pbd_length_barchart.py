# Author/s: Yee Chuen Teh
# Title: pbd_length_barchart.py
# Project: Chowdhury Lab Viral Escape
# Description: TODO: Description
# Reference:
'''
TODO: write your reference here
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
import argparse
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def fas_to_list(path):
    with open (path, "r") as f:
        a_temp = f.read()
        b_temp = a_temp.split("\n")
        if b_temp[len(b_temp)-1] == "":
            b_temp.pop()
        return b_temp

def convertfas(fas_list):
    seq_list = []
    name_list = []
    sequence = ""
    for p in fas_list:
        if p == "":
            continue
        if p[0] == ">":
            if sequence != "":
                seq_list.append(sequence)
                sequence = ""
            name_list.append(p)
        else:
            sequence += p
    seq_list.append(sequence)
    name_list.append(p)
    return [name_list, seq_list]

def barchart(c_temp, target_length):
    seq = c_temp[1]
    dict = {}
    target = 0
    for s in seq:
        length = len(s)
        if length <= target_length:
            target+=1
            if length in dict:
                dict[length]+=1
            else:
                dict[length] = 1

    myKeys = list(dict.keys())
    myKeys.sort()
    data = {i: dict[i] for i in myKeys}

    # create bar chart
    plt.bar(data.keys(), data.values(), color='g')

    # add labels and title
    plt.xlabel('Protein with sequence of length')
    plt.ylabel('frequency')
    plt.title('Bar Chart of Protein Sequence Length frequency.')

    frac = int(target)/int(len(seq))
    percentile = frac*100
    print("percentile of protein under length {}: {}".format(str(target_length), str(percentile)))
    # show plot
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, required=True)
    parser.add_argument('--c', type=int, required=True)
    parser.add_argument('--l', type=int, required=False)
    args = parser.parse_args()

    f_path = args.f
    a_temp = f_path.split("/")
    dir = a_temp[0]
    global name
    if "." in a_temp[1]:
        b_temp = a_temp[1].split(".")
        name = b_temp[0]
    else:
        name = a_temp[1]

    path = os.getcwd()
    to_path = path+"/"+dir
    os.chdir(to_path)

    fas_list = fas_to_list(a_temp[1])
    c_temp = convertfas(fas_list)
    if "--l" in sys.argv:
        barchart(c_temp, args.l)
    else:
        barchart(c_temp, -1)


    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<pbd_length_barchart.py>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<pbd_length_barchart.py>\" script --------------------\n")