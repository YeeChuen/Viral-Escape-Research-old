# Author/s: Yee Chuen Teh
# Title: pairwise.py
# Project: Chowdhury Lab Viral Escape
# Description: TODO: Description
# Reference:
'''
TODO: write your reference here
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
import re
import numpy as np
import matplotlib.pyplot as plt

#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here

def parse_fasta(filename):
    names, sequences = [], []
    with open(filename, "r") as f:
        name = None
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    names.append(name)
                    sequences.append(seq)
                name = line[1:]
                seq = ""
            else:
                seq += line
        if name:
            names.append(name)
            sequences.append(seq)
    return names, sequences

def pairwise_score(sequences):
    num_proteins = len(sequences)
    scores = np.zeros((num_proteins, num_proteins))
    for i in range(num_proteins):
        for j in range(i+1, num_proteins):
            # calculate pairwise score here
            score = 0
            scores[i, j] = score
            scores[j, i] = score
    return scores

def plot_heatmap(data, names):
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(data.shape[0]))
    ax.set_yticks(np.arange(data.shape[1]))
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)
    plt.xticks(rotation=90)
    plt.tight_layout()
    im = ax.imshow(data, cmap="viridis", aspect='equal')
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, "{:.2f}".format(data[i, j]), ha="center", va="center", color="w")
    plt.show()

def main():
    names, sequences = parse_fasta("PoreDB_short.fas")
    num_proteins = len(sequences)
    scores = pairwise_score(sequences)
    plot_heatmap(scores, names)
    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<PYTHON SCRIPT TITLE>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<PYTHON SCRIPT TITLE>\" script --------------------\n")