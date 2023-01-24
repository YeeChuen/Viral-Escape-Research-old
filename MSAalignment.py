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
from selenium.webdriver.common.keys import Keys
import time
import os.path
import csv
import pyperclip as pc
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService

#____________________________________________________________________________________________________
# set ups 

def MSATool(input, driver):
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.LINK_TEXT, "Search"))).click()
    time.sleep(2)
    # potential stuck on home page screen
    
    print("--- inputing PDB sequence ---")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
    elem = driver.find_element(By.TAG_NAME, 'textarea')
    pc.copy(input)
    elem.send_keys(Keys.CONTROL, 'v')
    # the button being in view also affect if it becomes clickable
    driver.execute_script("window.scrollTo(0, 300)") 
    
    print("--- submitting input ---")
    #if website xpath changes, or if code fails, check the xpath here
    xpath = '/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[1]/fieldset/div/button'
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    
    time.sleep(5)
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
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH, FASTA))).click()

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

    #return list here
    return list_2d

def MSA(csvfile, no_protein, file, MSAlink, compare_data):
    pbd_data = csv_to_list(csvfile)
    string = compare_data[2] + "\n" + compare_data[3] +"\n"
    compare_string = string
    count = 0
    inputstring = compare_string
    # Basecase:
    # count = 0
    # inputstring = compare_string
    pbd_list_2d = []

    #open browswer here
    print("--- opening broswer ---")
    driver = webdriver.Chrome()
    driver.get(MSAlink)

    for i in range(1,len(pbd_data)):
        string = pbd_data[i][2] + "\n" + pbd_data[i][3] +"\n"
        inputstring += string
        count+=1
        if count == no_protein or i == len(pbd_data)-1:
            print("\n---------- MSA for PBD {} to {} ----------".format(str(i-no_protein+1), str(i)))
            starttime = time.time()
            #with open('current.txt', 'w') as f:
            #    f.write(inputstring)
            templist = MSATool(inputstring, driver)
            print("total time: {}s".format(str(time.time()-starttime)))
            for list in templist:
                pbd_list_2d.append(list)
            #reset to base case
            save(pbd_list_2d, file)
            count = 0
            inputstring = compare_string
            pbd_list_2d=[]

    driver.close()

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

def main(): 
    csvfile = "PoreDB.csv"
    no_protein = 3999
    MSAlink = "https://toolkit.tuebingen.mpg.de/tools/hhblits"
    MSA(csvfile, no_protein, "MSA_long_0", MSAlink, csv_to_list("PoreDB_long.csv")[1])
    short_list = csv_to_list("PoreDB_short.csv")
    for i in range(1,len(short_list)):
        MSA(csvfile, no_protein, "MSA_short_{}".format(str(i-1)), MSAlink, short_list[i])
    


#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"MSAalignment.py\" script --------------------")
    main()
    print("-------------------- END of \"MSAalignment.py\" script --------------------\n")