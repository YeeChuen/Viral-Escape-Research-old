# Author/s: Yee Chuen Teh
# Title: MSAalignment.py
# Project: ChowdhuryLab Datamining from website
# Description: python script to for web automation to use MSA tool online from a given website
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
import urllib3
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os.path

#____________________________________________________________________________________________________
# set ups 

def MSAalignment(input):
    print("--- opening broswer ---")
    driver = webdriver.Chrome()
    driver.get("https://toolkit.tuebingen.mpg.de/tools/msaprobs")
    time.sleep(2)

    print("--- input PDB sequence to MSA form ---")
    elem = driver.find_element(By.TAG_NAME, 'textarea')
    elem.send_keys(input)
    # the button being in view also affect if it becomes clickable
    driver.execute_script("window.scrollTo(0, 300)") 
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

    time.sleep(2)
    http.clear()
    driver.close()

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"MSAalignment.py\" script --------------------")
    csvfile = "PBD_SequenceDF.csv"
    if not os.path.exists(csvfile):
        print("Unable to locate \"{}\".".format(csvfile))
        print("Make sure to run \"python pbd_dataframe.py\" to generate the csv file before \"MSAalignment.py\".")
        pass
    else:
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
        MSAalignment(param[1])

    print("-------------------- END of \"MSAalignment.py\" script --------------------\n")