# Author/s: Yee Chuen Teh
# Title: pbd_dataframe.py
# Project: ChowdhuryLab Datamining from website
# Description: python script to mine protein sequence and PDB ids from webs

#____________________________________________________________________________________________________
# imports 
import pandas as pd
import requests
import urllib3

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
    http = urllib3.PoolManager()
    fronturl = "https://www.rcsb.org/fasta/entry/"
    backurl = "/display"
    # a 2d list to store PBD id in list[0] and its sequence in list[1]
    pbdAndSequence = [[],[]]
    for pbd in pbdlist:
        id = str(pbd).replace(" ","")
        url = fronturl + id + backurl
        web_data = http.request('GET', url)
        text_data = web_data.data.decode('utf-8')
        text_data_list = text_data.splitlines()
        # some PBDid has been removed, check here checks if the current pbd is removed.
        check = text_data_list[0].split(" ")
        if check[0] == "No":
            print(text_data + " (PBDid: "+ id + ")")
        else:
            for i in range(0, len(text_data_list), 2):
                sequence = text_data_list[i+1]
                pbd_info = text_data_list[i].replace(">", "")
                pbd_info_list = pbd_info.split("|")
                pbd_id = pbd_info_list[0]
                pbdAndSequence[0].append(pbd_id)
                pbdAndSequence[1].append(sequence)
    return pbdAndSequence
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
    pbd_list = extract_pbd(PDB_list_2d)     # pbd_list contain all pbd id from above url

    # extract protein sequence from all PBDIDs in the pbd_list
    pbd_sequence_list = get_sequence(pbd_list)
    print(pbd_sequence_list)
    
    print("----------------------------------------------")