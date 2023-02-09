# Author/s: Yee Chuen Teh
# Title: pbd_checkdash.py (update as of 2/8/2023)
# Project: Chowdhury Lab Viral Escape
# Description: this script look for the target protein in the msa folder (output)
# Reference:
'''
TODO: write your reference here
usage: 
python pbd_checkdash.py --p muscle_long_1/3W5B_1_output --id 5YX9_1
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
from pbd_length import *
import numpy as np

#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here

def get_targetproteinfile(name):
    n_list = name.split("_")
    pid = n_list[len(n_list)-2]
    pid_no = n_list[len(n_list)-1]
    return pid + "_" +pid_no

def split_alph_dash(sequence):
    '''
    input:
        - any protein sequence (string type)

    output:
        - return a list, index 0 consist of number of alphabets, index 1 consist of number of dashes
    '''
    alph = 0
    dash = 0
    for char in sequence:
        if char == "-":
            dash+=1
        else:
            alph+=1
    return [alph, dash]

def plot_2d(seq_list, longname, alignname):
    '''
    input:
        - argument <seq_list> is a list of size 2, index 0 contain the longest sequence, index 1 contain the target sequence

    output:
        - do a 2D plot where
            - x-axis: the number of letters in target sequence (exclude dashes)
            - y-axis: the number of dashes in long sequence (only dashes)
    '''
    target_alph = split_alph_dash(seq_list[1])[0]
    long_dash = split_alph_dash(seq_list[0])[1]

    print("target sequence has alphabet of: {}".format(str(target_alph)))
    print("longest sequence has dashes of: {}".format(str(long_dash)))

    x = [target_alph]
    y = [long_dash]

    plt.scatter(x, y)
    plt.xlabel('size of aligned protein (excluding "-")')
    plt.ylabel('number of dashes in the long protein')
    plt.title('no. dashes in {} and original size of {}'.format(longname, alignname))
    plt.xticks([target_alph-2, target_alph-1, target_alph, target_alph+1, target_alph+2])
    plt.yticks([long_dash-2, long_dash-1, long_dash, long_dash+1, long_dash+2])
    plt.show()

def extract_name(fas_list):
    name_list = []
    for i in range(0,len(fas_list), 2):
        description = fas_list[i]
        n_list = description.split("|")
        name = n_list[0]
        truename = name.replace(">","")
        name_list.append(truename)
    return name_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', type=str, required=True)     # path location to the directory that store all output msa
    parser.add_argument('--id', type=str, required=True)     # the protein ID of the target protein. exp "ABCD_1"
    args = parser.parse_args()

    path = args.p
    target_protein = args.id
    output_list = os.listdir(path)

    target_file = ""
    for f in output_list:
        if get_targetproteinfile(f) == target_protein:
            target_file = f
            break

    file_path = path + "/"+target_file
    a_temp = fas_to_list(file_path)
    b_temp = split_des_seq(a_temp)
    name_list = extract_name(b_temp[0])
    seq_list = b_temp[1]
    plot_2d(seq_list, name_list[0], name_list[1])


    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<pbd_checkdash.py>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<pbd_checkdash.py>\" script --------------------\n")