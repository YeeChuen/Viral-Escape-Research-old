# Author/s: Yee Chuen Teh
# Title: pbd_scatter_dash.py 
# Project: Chowdhury Lab Viral Escape
# Description: this script look for the target protein in the msa folder (output)
# Reference:
'''
TODO: write your reference here
Usage: 
python pbd_scatter_dash.py --p muscle_long_1/3W5B_1_output --id 5YX9_1  (use "all" to do scatter plot for all)
'''
# Updates:  (2/9/2023)
'''
TODO: write your updates here
(2/9/2023)
    - update pbd_scatter_dash.py to plot scatter chart for all alignment pair
date
    - some update on this date
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
from tqdm import tqdm
import time
import math

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

def closest_multiple_of_10(n):
    quotient = n // 10
    upper = (quotient + 1) * 10
    lower = quotient * 10
    return lower if n - lower < upper - n else upper

def plot_2d(seq_list, longname, alignname):
    '''
    input:
        - argument <seq_list> is a list of size 2, index 0 contain the longest sequence, index 1 contain the target sequence

    output:
        - do a 2D plot where
            - x-axis: the number of letters in target sequence (exclude dashes)
            - y-axis: the number of dashes in long sequence (only dashes)
    '''
    x = []
    y = []
    x_min = sys.maxsize
    x_max = 0
    y_min = sys.maxsize
    y_max = 0
    if len(seq_list) == 2:
        target_alph = split_alph_dash(seq_list[1])[0]
        long_dash = split_alph_dash(seq_list[0])[1]
        x.append(target_alph)
        y.append(long_dash)
        x_min = min(x_min, target_alph)
        x_max = max(x_max, target_alph)
        y_min = min(y_min, long_dash)
        y_max = max(y_max, long_dash)
    else:
        for i in range(0,len(seq_list),2):
            target_alph = split_alph_dash(seq_list[i+1])[0]
            long_dash = split_alph_dash(seq_list[i])[1]
            x.append(target_alph)
            y.append(long_dash)
            x_min = min(x_min, target_alph)
            x_max = max(x_max, target_alph)
            y_min = min(y_min, long_dash)
            y_max = max(y_max, long_dash)

    x_diff = closest_multiple_of_10(math.floor((x_max-x_min)/10))
    y_diff = closest_multiple_of_10(math.floor((y_max-y_min)/10))

    plt.scatter(x, y, s=10)
    plt.xlabel('size of aligned protein (excluding "-")')
    plt.ylabel('number of dashes in the long protein {}'.format(longname))
    plt.title('scatter plot of no. dashes in {} and original size of {}'.format(longname, alignname))
    plt.xticks(np.arange(x_min, x_max+x_diff, x_diff))
    plt.yticks(np.arange(y_min, y_max+y_diff, y_diff))
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

    if target_protein == "all":
        all_fas = []
        for i in tqdm(range(0, len(output_list)),
               desc="Fetching MSA data...",
               ascii=False, ncols=100):
            file_path = path + "/" + output_list[i]
            a_temp = fas_to_list(file_path)
            for i in a_temp:
                all_fas.append(i)
            time.sleep(0.0001)
        b_temp = split_des_seq(all_fas)
        name_list = extract_name(all_fas)
        seq_list = b_temp[1]
        plot_2d(seq_list, name_list[0], "aligned pb")

    else:
        target_file = ""
        for f in output_list:
            if get_targetproteinfile(f) == target_protein:
                target_file = f
                break

        file_path = path + "/"+target_file
        a_temp = fas_to_list(file_path)
        b_temp = split_des_seq(a_temp)
        name_list = extract_name(a_temp)
        print(name_list)
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