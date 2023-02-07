# Author/s: Yee Chuen Teh
# Title: heatmap.py
# Project: Chowdhury Lab Viral Escape
# Description: TODO: Description
# Reference:
'''
TODO: write your reference here
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


#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def heatmap(seq_list, list_2d, start, end, size):
    tvalue = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    lvalue = ['R','H','K','D','E','S','T','N','Q','C','G','P','A','V','I','L','M','F','Y','W','U','X']
    x = np.arange(0,size,1)
    xvalue = []
    for i in range(start,end):
        xvalue.append(str(i))

    for seq in seq_list:
        for i in range(start, end):
            if seq[i] == '-':
                continue
            j = lvalue.index(seq[i])
            list_2d[j][i-start]+=1

    #plt.imshow(list_2d, cmap='hot', interpolation='nearest', origin='lower')
    #plt.yticks(ticks = tvalue, labels=lvalue)
    #plt.show()

    fig, ax = plt.subplots()
    plt.setp(ax, yticks=tvalue, yticklabels=lvalue, xticks=x, xticklabels = xvalue)
    ax.tick_params(axis='x', rotation=60)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    im = ax.imshow(list_2d, cmap='viridis',interpolation='nearest', origin='lower')
    fig.colorbar(im, cax=cax, orientation='vertical')
    for i in range(len(tvalue)):
        for j in range(size):
            ax.annotate(str(list_2d[i][j]), xy=(j, i), ha="center", va="center", fontsize=6, color='red')
            rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
    ax.set_title("Frequency of Protein Residue Type in Sequence Index out of {} sequence".format(str(len(seq_list))))

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

def main():
    hm_list = []
    file = "Muscle_4UG0_1_length_5070"
    with open(file, 'r') as f:
        read = f.read()
        hm_list = read.split("\n")
        hm_list.pop()

    seq = only_seq(hm_list)
    start = 30
    end = 50
    size = end-start
    list_2d = [[0 for i in range(size)] for i in range(22)] 
    heatmap(seq, list_2d, start, end, size)

    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<PYTHON SCRIPT TITLE>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<PYTHON SCRIPT TITLE>\" script --------------------\n")