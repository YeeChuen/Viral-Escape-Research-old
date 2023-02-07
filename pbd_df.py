# Author/s: Yee Chuen Teh
# Title: pbd_dataframe.py
# Project: ChowdhuryLab Datamining from website
# Description: python script to mine protein sequence and PDB ids from webs
# Reference:
'''A Completely Reimplemented MPI Bioinformatics Toolkit with a New HHpred Server at its Core.
Zimmermann L, Stephens A, Nam SZ, Rau D, Kübler J, Lozajic M, Gabler F, Söding J, Lupas AN, Alva V. J Mol Biol. 2018 Jul 20. S0022-2836(17)30587-9.

Protein Sequence Analysis Using the MPI Bioinformatics Toolkit.
Gabler F, Nam SZ, Till S, Mirdita M, Steinegger M, Söding J, Lupas AN, Alva V. Curr Protoc Bioinformatics. 2020 Dec;72(1):e108. doi: 10.1002/cpbi.108.

HHblits: lightning-fast iterative protein sequence searching by HMM-HMM alignment.
Remmert M, Biegert A, Hauser A, Söding J. Nat Methods. 2011 Dec 25;9(2):173-5.'''

#____________________________________________________________________________________________________
# imports 
import pandas as pd
import requests
import urllib3
from tqdm import tqdm
import time

#____________________________________________________________________________________________________
# functions 

# extract all PBD_ids into a list
def extract_pbd(PDB_list_2d):
    print("--- extracting PBD ids ---")

    pbdlist = []
    for x in tqdm(range(2, len(PDB_list_2d)),
               desc="Extracting PBD ids...",
               ascii=False, ncols=75):
        templist = PDB_list_2d[x].split("PBDID: ")
        for y in range(1, len(templist)):
            # make sure there is no duplicate PBDid in the list
            if templist[y] not in pbdlist:
                pbdlist.append(templist[y])
                
        time.sleep(0.001)
    return pbdlist


# extract all protein sequence from all PBD_ids
def get_sequence(pbdlist):
    print("--- retrieving PBD sequence ---")

    http = urllib3.PoolManager()
    fronturl = "https://www.rcsb.org/fasta/entry/"
    backurl = "/display"
    pbdAndSequence = []     # a 2d list to store PBD id in list[0] and its sequence in list[1]
    longest = []            # store the longest sequence in the list
    shortest = []           # a shortest sequence in the list
    ux50 = []               # store sequence with 50% or more U or X
    ux100 = []              # store sequence with 100% U or X
    duplicates = []         # store duplicate sequence
    less_15 = []            # store sequence with less than 15 length
    short_list = []         # store shortest sequence 
    long_list = []         # store shortest sequence 
    memory = set()

    for i in tqdm(range(len(pbdlist)),
               desc="Retrieving protein data...",
               ascii=False, ncols=75):
        id = str(pbdlist[i]).replace(" ","")
        url = fronturl + id + backurl
        web_data = http.request('GET', url)
        text_data = web_data.data.decode('utf-8')
        text_data_list = text_data.splitlines()
        # some PBDid has been removed, check here checks if the current pbd is removed.
        check = text_data_list[0].split(" ")
        if check[0] == "No":
            continue
        else:
            for i in range(0, len(text_data_list), 2):
                sequence = text_data_list[i+1]
                # check for duplicates
                checkduplicate = len(memory)
                memory.add(str(sequence))                
                templist = []
                templist.append(text_data_list[i])
                templist.append(sequence)

                if checkduplicate == len(memory):
                    duplicates.append(templist)
                    continue

                if len(str(sequence)) >= 15:
                    if count_ux(str(sequence)) == 1:
                        ux100.append(templist)
                    elif  count_ux(str(sequence)) >= 0.5:
                        ux50.append(templist)
                    else:    
                        if not shortest:
                            shortest = templist
                            short_list.append(shortest)
                        elif len(shortest[1]) == len(templist[1]):
                            shortest = templist
                            short_list.append(shortest)
                        elif len(shortest[1]) > len(templist[1]):
                            short_list.clear()
                            shortest = templist
                            short_list.append(shortest)

                        if not longest:
                            longest = templist
                            long_list.append(longest)
                        elif len(longest[1]) == len(templist[1]):
                            longest = templist
                            long_list.append(longest)
                        elif len(longest[1]) < len(templist[1]):
                            long_list.clear()
                            longest = templist
                            long_list.append(longest)

                        pbdAndSequence.append(templist)
                else:
                    less_15.append(templist)
    http.clear()
    return [pbdAndSequence,long_list,short_list, ux100, ux50, duplicates, less_15]

def count_ux(sequence):
    ux = 0
    for char in sequence:
        if char == 'U' or char == 'X':
            ux+=1
    return (ux/len(sequence))

def convertfas(list_2D, filename): 
    with open(filename, 'w') as f:
        for i in tqdm(range(len(list_2D)),
               desc="Exporting to {}...".format(filename),
               ascii=False, ncols=75):
            for j in list_2D[i]:
                f.write(j+"\n")
            time.sleep(0.001)

def main():
    # url variable 
    url1 = "https://tcdb.org/search/index.php?query=&type=pdb"

    # extraction of PBD_ids into list
    html = requests.get(url1).content
    df = pd.read_html(html)
    PDB_list_2d = df[0][2]
    pbd_list = extract_pbd(PDB_list_2d)     # pbd_list contain all pbd id from above url

    # extract protein sequence from all PBDIDs in the pbd_list
    return_list = get_sequence(pbd_list)
    pbd_sequence_list = return_list[0]      #this is just reference, not a copy
    longest = return_list[1]                # longest sequence will be used to be compared during MSA
    shortest = return_list[2]               # shortest sequence from PDB
    ux100 = return_list[3]                  # ux100 sequence from PDB
    ux50 = return_list[4]                   # ux50 sequence from PDB
    duplicates = return_list[5]             # duplicates sequence from PDB
    less_15 = return_list[6]                # lessthan 15 length sequence from PDB

    print("--- exporting data to .fas format files ---")
    convertfas(longest, 'PoreDB_long.fas')
    convertfas(shortest, 'PoreDB_short.fas')
    convertfas(pbd_sequence_list, 'PoreDB.fas')
    convertfas(ux100, 'PoreDB_100ux.fas')
    convertfas(ux50, 'PoreDB_50ux.fas')
    convertfas(duplicates, 'PoreDB_duplicates.fas')
    convertfas(less_15, 'PoreDB_less15.fas')

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"pbd_dataframe.py\" script --------------------")
    main()
    print("-------------------- END of \"pbd_dataframe.py\" script --------------------\n")
