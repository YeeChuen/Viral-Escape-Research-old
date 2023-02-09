# Author/s: Yee Chuen Teh
# Title: pbd_heatmap.py (update as of 2/8/2023)
# Project: Chowdhury Lab Viral Escape
# Description: Warning, this script only handle FAS file where the sequence is atleast 100 in length, and all length is the same
#               produce heatmap given a selected fas file
# Reference:
'''
TODO: write your reference here
Usage: 
python pbd_heatmap.py --f PoreDB_nonRNA/Muscle_3W5B_1_eq1000.fas --s 0 --r 50
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import numpy as np
import random
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
import copy
import argparse


#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def heatmap(list_2d, start, end, size, seq_length):
    tvalue = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    lvalue = ['R','H','K','D','E','S','T','N','Q','C','G','P','A','V','I','L','M','F','Y','W','U','X']
    x = np.arange(0,size,1)
    xvalue = []
    for i in range(start,end):
        xvalue.append(str(i))

    reversed_list = list(map(list, zip(*list_2d)))
    data = [[0 for i in range(size)] for i in range(22)] 
    for i in range(len(reversed_list)):
        for j in range(start,end):
            data[i][j-start] = reversed_list[i][j]
            
    #plt.imshow(data, cmap='hot', interpolation='nearest', origin='lower')
    #plt.yticks(ticks = tvalue, labels=lvalue)
    #plt.show()

    fig, ax = plt.subplots()
    plt.setp(ax, yticks=tvalue, yticklabels=lvalue, xticks=x, xticklabels = xvalue)
    ax.tick_params(axis='x', rotation=60)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    im = ax.imshow(data, cmap='viridis',interpolation='nearest', origin='lower')
    fig.colorbar(im, cax=cax, orientation='vertical')
    for i in range(len(tvalue)):
        for j in range(size):
            ax.annotate(str(data[i][j]), xy=(j, i), ha="center", va="center", fontsize=6, color='red')
            rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
    ax.set_title("Frequency of Protein Residue Type in Sequence Index out of {} sequence".format(str(seq_length)))

    fig.tight_layout()
    plt.show()

    pass

def only_seq(hm_list):
    a = []
    for hm in hm_list:
        if hm == "" or hm[0] == ">":
            continue
        else:
            a.append(hm)
    return a

def normalize(seq_list):
    #seq_dict = {'R':0,'H':0,'K':0,'D':0,'E':0,'S':0,'T':0,'N':0,'Q':0,
    #'C':0,'G':0,'P':0,'A':0,'V':0,'I':0,'L':0,'M':0,'F':0,'Y':0,'W':0,'U':0,'X':0}
    
    seq_dict = {'R':0,'H':1,'K':2,'D':3,'E':4,'S':5,'T':6,'N':7,'Q':8,
    'C':9,'G':10,'P':11,'A':12,'V':13,'I':14,'L':15,'M':16,'F':17,'Y':18,'W':19,'U':20,'X':21}

    same_length = len(seq_list[0])
    norm_list = [[0 for i in range(len(seq_dict))] for i in range(100)]
    a_temp = [0 for i in range(len(seq_dict))]
    print("sequence length of: {}".format(str(len(seq_list[0]))))
    norm = math.floor(same_length/100)

    if norm >= 1:
        for s in seq_list:
            if same_length != len(s):
                print("check FASTA file sequence, must be in same length")
                break
            condense = True
            n_index = 0
            counter = -1
            percent = 1
            for i in range(len(s)):
                #print("iter {}".format(str(i)))
                #print("counter: {}".format(str(counter)))
                if s[i] == "-":
                    continue
                norm_list[n_index][seq_dict[s[i]]]+=1
                if condense == True:
                    if (len(s))%(100) == n_index:
                        condense = False
                        counter = 0

                if counter+1 == norm or i == len(s)-1:
                    #print("load into percentile: {}".format(str(percent)))
                    if condense == True:
                        counter = -1
                    else:
                        counter = 0
                    percent+=1
                    n_index+=1
                else:
                    counter +=1
    else:
        for s in seq_list:
            for i in range(len(s)):
                if s[i] == "-":
                    continue
                #print("iter {}".format(str(i)))
                #print("counter: {}".format(str(counter)))
                norm_list[i][seq_dict[s[i]]]+=1

    #print(norm_list)

    return norm_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, required=True)     # path location to the file
    parser.add_argument('--s', type=int, required=True)     # start index to plot
    parser.add_argument('--r', type=int, required=True)     # range of plot
    args = parser.parse_args()

    hm_list = []
    file = args.f
    with open(file, 'r') as f:
        read = f.read()
        hm_list = read.split("\n")
        hm_list.pop()

    seq_dict = {'R':0,'H':1,'K':2,'D':3,'E':4,'S':5,'T':6,'N':7,'Q':8,
    'C':9,'G':10,'P':11,'A':12,'V':13,'I':14,'L':15,'M':16,'F':17,'Y':18,'W':19,'U':20,'X':21}

    seq_list = only_seq(hm_list)
    norm_list = normalize(seq_list)

    start = args.s  #0 is ther first
    end = start+args.r    # end-1 is the actual end (exp, 99)
    size = end-start
    #list_2d = [[0 for i in range(size)] for i in range(22)] 

    if start >= 100:
        print("invalid start percentile, choose in between 0 to 99")
        return
    if start + args.r > 100:
        end = 100
        size = end-start

    heatmap(norm_list, start, end, size, len(seq_list[0]))

    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<pbd_heatmap.py>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<pbd_heatmap.py>\" script --------------------\n")