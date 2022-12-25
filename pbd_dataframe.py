# Author/s: Yee Chuen Teh
# Title: pbd_dataframe.py
# Project: ChowdhuryLab Datamining from website
# Description: python script to mine protein sequence and PDB ids from webs

#____________________________________________________________________________________________________
# imports 
import pandas as pd
import requests

#____________________________________________________________________________________________________
# functions 

# extract all PBD_ids into a list
def extract_pbd(PDB_list_2d):
    pbdlist = []
    for x in range(2, len(PDB_list_2d)):
        templist = PDB_list_2d[x].split("PBDID: ")
        for y in range(1, len(templist)):
            pbdlist.append(templist[y])
    return pbdlist


# extract all protein sequence from all PBD_ids
def get_sequence(pbdlist):
    fronturl = "https://www.rcsb.org/fasta/entry/"
    backurl = "/display"
    # a 2d list to store PBD id in list[0] and its sequence in list[1]
    pbdAndSequence = [[],[]]
    for pbd in pbdlist:
        url = fronturl + str(pbd) + backurl
    return -1
# add both into a new dataframe

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("-------------------- MAIN --------------------")
    
    # url variable 
    url = "https://tcdb.org/search/index.php?query=&type=pdb"

    # extraction of PBD_ids into list
    html = requests.get(url).content
    df = pd.read_html(html)
    PDB_list_2d = df[0][2]
    pbdlist = extract_pbd(PDB_list_2d)
    print(pbdlist[0:3])
    print(len(pbdlist))
    
    print("----------------------------------------------")