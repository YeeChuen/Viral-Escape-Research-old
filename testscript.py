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
from selenium.webdriver.common.action_chains import ActionChains
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

def main(input):
    print("--- opening broswer ---")
    driver = webdriver.Chrome()
    driver.get("https://toolkit.tuebingen.mpg.de/tools/msaprobs")
    time.sleep(2)

    print("--- input PDB sequence to MSA form ---")
    elem = driver.find_element(By.TAG_NAME, 'textarea')
    elem.send_keys(input)
    # the button being in view also affect if it becomes clickable
    driver.execute_script("window.scrollTo(0, 200)") 
    time.sleep(2)

    print("--- locating submit button ---")
    #if website xpath changes, or if code fails, check the xpath here
    xpath = '/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[1]/fieldset/div/button'
    button = driver.find_element(By.XPATH, xpath)
    button.click()
    time.sleep(2)

    print("--- Querying Job for MSA alignment ---")
    # driver move to the new webpage
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)
    # check if the job exists, if yes, prompt driver to click load job
    queued = "Your submission is queued!"
    processed = "Your submission is being processed!"
    exists = "We found an identical copy of your job in our database!"
    if queued in driver.page_source:
        while queued in driver.page_source:
            pass
        while processed in driver.page_source:
            pass
        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)
        time.sleep(2)
    elif exists in driver.page_source:
        xpath = "/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[3]/div/div/button[2]"
        loadjob = driver.find_element(By.XPATH, xpath)
        loadjob.click()
        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)
        time.sleep(2)
    FASTA = "/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[1]/ul/li[4]/a"
    FASTAbutton = driver.find_element(By.XPATH, FASTA)
    FASTAbutton.click()
    time.sleep(2)

    print("--- Obtaining MSA result ---")
    exportlocation = "/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[4]/div[1]/div[1]/a[4]"
    export = driver.find_element(By.XPATH, exportlocation)
    exportlink = export.get_attribute('href')
    print("--- MSA job result URL: {}".format(exportlink))
    strUrl = driver.current_url
    print("--- Job URL: {}".format(strUrl))
    http = urllib3.PoolManager()
    web_data = http.request('GET', exportlink)
    text_data = web_data.data.decode('utf-8')
    print("Results:\n{}".format(text_data))

    time.sleep(100)
    http.clear()
    driver.close()

def getFASTA(exportlink):
    http = urllib3.PoolManager()
    web_data = http.request('GET', exportlink)
    text_data = web_data.data.decode('utf-8')
    list_data = text_data.split("\n")
    list_2d = []
    templist = []
    tempstring = ""
    for data in list_data:
        print(data)
        if ">" in data:
            if tempstring != "":
                templist.append(tempstring)
                list_2d.append(templist)
                templist = []
                tempstring = ""
            templist.append(data)
        else:
            tempstring += data
    
    for list in list_2d:
        for entry in list:
            print(entry)

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
            \nGREQERRGHFVRFDRLERMLDDNRR\
            \n>1J95_1|Chains A, B, C, D|VOLTAGE-GATED POTASSIUM CHANNEL|Streptomyces lividans (1916)\
            \nMPPMLSGLLARLVKLLLGRHGSALHWRATLWGRCVAVVVMVALATWFVGREQERRGHF\
            \n>1JQ1_1|Chains A, B, C, D|VOLTAGE-GATED POTASSIUM CHANNEL|Streptomyces lividans (1916)\
            \nLWGRCVAVVVMVAGITSFGLVTAALATWFVGREQ"
    }
    #print(param[1])

    # start test on selenium (web automation)
    #main(param[1])
    getFASTA("https://toolkit.tuebingen.mpg.de/api/jobs/2406460/results/files/alignment.fas")
    
    print("-------------------- END --------------------")

