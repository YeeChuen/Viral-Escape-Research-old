# Author/s: Yee Chuen Teh
# Title: pd_dataframe.py
# Project: ChowdhuryLab Datamining from website
# Description: python script to mine protein sequence and PDB ids from webs

#____________________________________________________________________________________________________
# imports 
import pandas as pd
import urllib3
import requests

#____________________________________________________________________________________________________
# set ups 

# set up pandas and urllib3 variable to use
#df = pd.DataFrame()
#http = urllib3.PoolManager()

# url variable 
#url = "https://tcdb.org/search/index.php?query=&type=pdb"

#web_data = http.request('GET', url)


# try only using pandas
#tables_on_page = pd.read_html(url)
#table = tables_on_page[0]
#table.to_json("table.json", index=False, orient='table')

# 2nd try using pandas
#html = requests.get(url).content
#df = pd.read_html(html)
#PDB_ids_list = df[0][2]
#print(df)
#df.to_csv('my data.csv')

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("-------------------- MAIN --------------------")
    #print(urllib3.__version__)
    #print(PDB_ids_list)
    #print(web_data.data.decode('utf-8'))

    #print(tables_on_page)

    
    url = "https://www.rcsb.org/fasta/entry/2ITC/display"
    html = requests.get(url).content
    df = pd.read_html(html)

    
    print("----------------------------------------------")

