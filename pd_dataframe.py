# Author/s: Yee Chuen Teh
# Title: pd_dataframe.py
# Project: ChowdhuryLab Datamining from website
# Description: python script to mine protein sequence and PDB ids from webs

#____________________________________________________________________________________________________
# imports 
import pandas as pd
import urllib3
import requests
from selenium import webdriver
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

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

# Try Selenium
class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://www.youtube.com/")
        #self.assertIn("YouTube", driver.title)

        elem = driver.find_element(By.ID, "sea")

        elem.send_keys("maplestory bgm")
        elem.send_keys(Keys.RETURN)
        time.sleep(5)

        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)

        elem = driver.find_element(By.NAME, "search_query")
        elem.send_keys("maplestory class")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)

        strUrl = driver.current_url
        print(strUrl)
        
        #self.assertNotIn("No results found.", driver.page_source)


    def tearDown(self):
        self.driver.close()

def main():
        driver = webdriver.Chrome()
        driver.get("https://www.youtube.com/")

        elem = driver.find_element(By.NAME, "search_query")

        elem.send_keys("maplestory bgm")
        elem.send_keys(Keys.RETURN)
        time.sleep(3)

        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)

        video = driver.find_element(By.LINK_TEXT, 'Maplestory BGM Compilation - Explorer\'s Journey to the Black Mage')
        video.click()
        time.sleep(60)

        strUrl = driver.current_url
        print("---")
        print(strUrl)
        print("---")

        driver.close()


#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("-------------------- MAIN --------------------")
    #print(urllib3.__version__)
    #print(PDB_ids_list)
    #print(web_data.data.decode('utf-8'))

    #print(tables_on_page)

    # sequence test
    http = urllib3.PoolManager()
    '''
    url = "https://www.rcsb.org/fasta/entry/1S33/display"
    web_data = http.request('GET', url)
    text_data = web_data.data.decode('utf-8')
    text_data_list = text_data.splitlines()
    check = text_data_list[0].split(" ")
    if check[0] == "No":
            print(text_data + " (for PBDid: "+ "1S33" + ")")
    else:
        for i in range(0, len(text_data_list), 2):
            sequence = text_data_list[i+1]
            pbd_info = text_data_list[i].replace(">", "")
            pbd_info_list = pbd_info.split("|")
            pbd_id = pbd_info_list[0]
            print(pbd_id)
            print(sequence)'''

    # Webautomation test
    url2 = "https://toolkit.tuebingen.mpg.de/tools/msaprobs"
    web_data = http.request('GET', url2)
    text_data = web_data.data.decode('utf-8')
    #print(text_data)
    param = {
        1: ">1F6G_1|Chains A, B, C, D|VOLTAGE-GATED POTASSIUM CHANNEL|Streptomyces lividans (1916)\
            \nMPPMLSGLLARLVKLLLGRHGSALHWAAAGAATVLLVIVLLAGSYLAVLAERGAPGAQLITYPAALWWSVETATTVGYGDLYPVTLWGRCVAVVVMVAGITSFGLVTAALATWFVGREQERRGHFVRHSEKAAEEAYTRTTRALHERFDRLERMLDDNRR\
            \n>1J95_1|Chains A, B, C, D|VOLTAGE-GATED POTASSIUM CHANNEL|Streptomyces lividans (1916)\
            \nMPPMLSGLLARLVKLLLGRHGSALHWRAAGAATVLLVIVLLAGSYLAVLAERGAPGAQLITYPRALWWSVETATTVGYGDLYPVTLWGRCVAVVVMVAGITSFGLVTAALATWFVGREQERRGHF\
            \n>1JQ1_1|Chains A, B, C, D|VOLTAGE-GATED POTASSIUM CHANNEL|Streptomyces lividans (1916)\
            \nLWGRCVAVVVMVAGITSFGLVTAALATWFVGREQ"
    }
    #print(param[1])

    # start test on selenium (web automation)
    main()
    
    print("----------------------------------------------")

