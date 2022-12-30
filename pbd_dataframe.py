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
            print("Scrapping data. (PBDid: {})".format(id))
            for i in range(0, len(text_data_list), 2):
                sequence = text_data_list[i+1]
                templist = []
                templist.append(id)
                templist.append(text_data_list[i])
                templist.append(sequence)
                if not longest:
                    longest = templist
                elif len(longest[2]) < len(templist[2]):
                    longest = templist
                pbdAndSequence.append(templist)
    http.clear()
    print("--- retrieval done PBD sequence ---")
    return [pbdAndSequence,longest]

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

    list = [longest]
    df = pd.DataFrame(list, columns =['PBD_id', 'PBD_info', 'PBD_Sequence']) 
    
    print("--- longest sequence ---")
    for x in range(len(longest)):
        if x == 0:
            print("PBDID: {}".format(str(longest[x])))
        if x == 1:
            print("PBD INFO: {}".format(str(longest[x])))
        if x == 2:
            print("PBD SEQUENCE: {}".format(str(longest[x])))
    df.to_csv('PBD_LSequence.csv')
    print("---")
    print("Note: extract longest sequence here to be used for MSA alignment, saved as \"PBD_LSequence.csv\"\
        \ncsvfile created: \"PBD_LSequence.csv\"\
        \nAll protein sequence will be used to align with this longest sequence.")
    print("--- end longest sequence ---")

    df = pd.DataFrame(pbd_sequence_list, columns =['PBD_id', 'PBD_info', 'PBD_Sequence']) 

    # save the df as a digital csv 
    df.to_csv('PBD_AllSequenceDF.csv')
    print("---")
    print("PBD dataframe created, saved as save as \"PBD_AllSequenceDF.csv\.")
    print("csvfile created: \"PBD_AllSequenceDF.csv\"")
    print("run \"python readcsv.py --fPath PBD_AllSequenceDF.csv\" on terminal to read csv file")
    print("OPTIONAL: run \"python readcsv.py --fPath PBD_AllSequenceDF.csv --search <PBDID>\" on terminal to search specific PBD")
    print("---")

    #url2 = "https://toolkit.tuebingen.mpg.de/tools/msaprobs"

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"pbd_dataframe.py\" script --------------------")
    main()
    print("-------------------- END of \"pbd_dataframe.py\" script --------------------\n")
