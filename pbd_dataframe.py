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
import os.path

#____________________________________________________________________________________________________
# functions 

# extract all PBD_ids into a list
def extract_pbd(PDB_list_2d):
    print("--- extracting PBD ids ---")

    pbdlist = []
    for x in range(2, len(PDB_list_2d)):
        templist = PDB_list_2d[x].split("PBDID: ")
        for y in range(1, len(templist)):
            # make sure there is no duplicate PBDid in the list
            if templist[y] not in pbdlist:
                pbdlist.append(templist[y])
                
    print("--- extraction done PBD ids ---")
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
    memory = set()
    for pbd in pbdlist:
        id = str(pbd).replace(" ","")
        url = fronturl + id + backurl
        web_data = http.request('GET', url)
        text_data = web_data.data.decode('utf-8')
        text_data_list = text_data.splitlines()
        # some PBDid has been removed, check here checks if the current pbd is removed.
        check = text_data_list[0].split(" ")
        if check[0] == "No":
            print(text_data + " (PBDid: {})".format(id))
        else:
            for i in range(0, len(text_data_list), 2):
                sequence = text_data_list[i+1]
                # check for duplicates
                checkduplicate = len(memory)
                memory.add(str(sequence))                
                templist = []
                templist.append(id)
                templist.append(text_data_list[i])
                templist.append(sequence)
                templist.append(len(str(sequence)))

                if checkduplicate == len(memory):
                    print("duplicate sequence, added to duplicates. (PBDid: {})".format(id))
                    duplicates.append(templist)
                    continue

                if len(str(sequence)) >= 15:
                    if count_ux(str(sequence)) == 1:
                        ux100.append(templist)
                        print("Scrapping data, added to PoreDB_100ux. (PBDid: {})".format(id))
                    elif  count_ux(str(sequence)) >= 0.5:
                        ux50.append(templist)
                        print("Scrapping data, added to PoreDB_50ux. (PBDid: {})".format(id))
                    else:    
                        if not shortest:
                            shortest = templist
                        elif len(shortest[2]) >= len(templist[2]):
                            shortest = templist
                            if len(shortest[2]) == 15:
                                short_list.append(shortest)                     
                        if not longest:
                            longest = templist
                        elif len(longest[2]) < len(templist[2]):
                            longest = templist
                        pbdAndSequence.append(templist)
                        print("Scrapping data, added to PoreDB. (PBDid: {})".format(id))
                else:
                    less_15.append(templist)
                    print("Protein sequence length <15. (PBDid: {})".format(id))
    http.clear()
    print("--- retrieval done PBD sequence ---")
    return [pbdAndSequence,longest,short_list, ux100, ux50, duplicates, less_15]

def count_ux(sequence):
    ux = 0
    for char in sequence:
        if char == 'U' or char == 'X':
            ux+=1
    return (ux/len(sequence))

def convertcsv(single_protein_list, filename):
    list = [single_protein_list]
    df = pd.DataFrame(list, columns =['PBD_id', 'PBD_info', 'PBD_Sequence', 'PBD_Sequence_length']) 
    print("--- converting single sequence into csv ---")
    df.to_csv(filename)
    print("---")
    print("csvfile created: \"{}\"".format(str(filename)))

def convercsv2d(protein_list_2D, filename):
    df = pd.DataFrame(protein_list_2D, columns =['PBD_id', 'PBD_info', 'PBD_Sequence', 'PBD_Sequence_length']) 
    # save the df as a digital csv 
    df.to_csv(filename)
    print("---")
    print("csvfile created: \"{}\"".format(str(filename)))


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

    convertcsv(longest, 'PoreDB_long.csv')
    convercsv2d(shortest, 'PoreDB_short.csv')
    convercsv2d(pbd_sequence_list, 'PoreDB.csv')
    convercsv2d(ux100, 'PoreDB_100ux.csv')
    convercsv2d(ux50, 'PoreDB_50ux.csv')
    convercsv2d(duplicates, 'PoreDB_duplicates.csv')
    convercsv2d(less_15, 'PoreDB_less15.csv')

    print("---")
    print("run \"python readcsv.py --fPath PoreDB.csv\" on terminal to read csv file")
    print("OPTIONAL: run \"python readcsv.py --fPath PoreDB.csv --search <PBDID>\" on terminal to search specific PBD")


#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"pbd_dataframe.py\" script --------------------")
    main()
    print("-------------------- END of \"pbd_dataframe.py\" script --------------------\n")
