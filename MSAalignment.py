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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import sys
import time
import os.path
import csv

#____________________________________________________________________________________________________
# set ups 

def MSATool(input):
    print("--- opening broswer ---")
    driver = webdriver.Chrome()
    driver.get("https://toolkit.tuebingen.mpg.de/tools/msaprobs")
    # potential stuck on home page screen
    
    print("--- inputing PDB sequence ---")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
    elem = driver.find_element(By.TAG_NAME, 'textarea')
    elem.send_keys(input)
    # the button being in view also affect if it becomes clickable
    driver.execute_script("window.scrollTo(0, 300)") 
    
    print("--- submitting input ---")
    #if website xpath changes, or if code fails, check the xpath here
    xpath = '/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[1]/fieldset/div/button'
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    
    time.sleep(2)
    # driver move to the new webpage
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)
    # check if the job exists, if yes, prompt driver to click load job
    queued = "Your submission is queued!"
    processed = "Your submission is being processed!"
    exists = "We found an identical copy of your job in our database!"
    if exists in driver.page_source:    
        print("--- loading job ---")
        xpath = "/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[3]/div/div/button[1]"
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    if queued in driver.page_source:
        print("--- job is queued ---")
        while queued in driver.page_source:
            pass
        if processed in driver.page_source:
            print("--- job is being processed ---")
            while processed in driver.page_source:
                pass

    print("--- fetching job results ---")
    FASTA = "/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[1]/ul/li[4]/a"
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, FASTA))).click()

    # potential stuck on loading hits... page
    time.sleep(1)
    loading = "Loading hits..."
    while loading in driver.page_source:
        start = time.time()
        while time.time() - start < 1:
            pass
        if time.time() - start >= 1:
            driver.refresh()
            FASTA = "/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[1]/ul/li[4]/a"
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, FASTA))).click()
        time.sleep(1)

    print("--- Obtaining MSA result ---")
    exportlocation = "/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[4]/div[1]/div[1]/a[4]"
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, exportlocation)))
    export = driver.find_element(By.XPATH, exportlocation)
    exportlink = export.get_attribute('href')

    print("--- MSA job result URL: {}".format(exportlink))
    strUrl = driver.current_url
    print("--- Job URL: {}".format(strUrl))
    http = urllib3.PoolManager()
    web_data = http.request('GET', exportlink)
    text_data = web_data.data.decode('utf-8')

    list_data = text_data.split("\n")
    list_2d = []
    templist = []
    tempstring = ""
    for data in list_data:
        if ">" in data:
            if tempstring != "":
                templist.append(tempstring)
                list_2d.append(templist)
                templist = []
                tempstring = ""
            templist.append(data)
        else:
            tempstring += data
    templist.append(tempstring)
    list_2d.append(templist)

    http.clear()
    driver.close()

    #return list here
    return list_2d

def MSA(csvfile, compare_long, mod, file):
    pbd_data = csv_to_list(csvfile)
    if compare_long == True:
        long_data = csv_to_list("PBD_LSequence.csv")
        longstring = ""
        for i in range(1,len(long_data)):
            string = long_data[i][2] + "\n" + long_data[i][3] +"\n"
            longstring += string
        count = 0
        inputstring = longstring
    # Basecase:
    # count = 0
    # inputstring = longstring
    else:
        count = 0
        inputstring = ""

    pbd_list_2d = []
    for i in range(1,len(pbd_data)):
        string = pbd_data[i][2] + "\n" + pbd_data[i][3] +"\n"
        inputstring += string
        count+=1
        if count == mod:
            templist = MSATool(inputstring)
            for list in templist:
                pbd_list_2d.append(list)
            #reset to base case
            save(pbd_list_2d, file)
            count = 0
            if compare_long == True:
                inputstring = longstring
            else:
                inputstring = ""
            pbd_list_2d=[]

def csv_to_list(csvfile):
    with open(csvfile) as file:
        reader = csv.reader(file, delimiter=',')
        return list(reader)

def save(list, file):
    # Check whether the specified path exists or not
    isExist = os.path.exists(file)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(file)

    path = os.getcwd()
    save_path = path + "\\" + file
    os.chdir(save_path)

    tracker = "tracker.txt"
    isExist = os.path.exists(tracker)
    global number
    if not isExist:
        with open('tracker.txt', 'w') as f:
            f.write('0')
            number = 0
    else:
        with open('tracker.txt', 'r') as f:
            number = int(f.read()) + 1
        with open('tracker.txt', 'w') as f:
            f.write(str(number))


    df = pd.DataFrame(list, columns =['PBD_info', 'PBD_Sequence']) 
    # save the df as a digital csv 
    csvname = str(number) + '_' + file + '.csv'
    df.to_csv(csvname)
    os.chdir(path)
    


#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"MSAalignment.py\" script --------------------")
    #TODO: MAKE SURE TO CHECK LONGEST OR COMPARE SEQUENCE
    csvfile = "PBD_AllSequenceDF.csv"

    if not os.path.exists(csvfile):
        print("Unable to locate \"{}\".".format(csvfile))
        print("Make sure to run \"python pbd_dataframe.py\" to generate the csv file before \"MSAalignment.py\".")
        pass
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('--m', type=str, required=True)
        parser.add_argument('--w', type=str, required=False)
        parser.add_argument('--c', type=str, required=False)
        parser.add_argument('--f', type=str, required=False)
        compare_long = False
        args = parser.parse_args()
        file = "MSA alignment files"
        if "--w" in sys.argv[1:]:
            if str(args.w) == "l":
                print("comparing with longest PBD")
                compare_long = True
                # TODO: if the compare PBD is not l, there is 1 PBD that other PBD will compare with.
        if "--f" in sys.argv[1:]:
            print("creating new file to store data")
            file = str(args.f)

        mod = int(args.m)

        #start test on selenium (web automation)
        list = MSA(csvfile, compare_long, mod, file)


    print("-------------------- END of \"MSAalignment.py\" script --------------------\n")