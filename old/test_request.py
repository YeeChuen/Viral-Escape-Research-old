# Author/s: Yee Chuen Teh
# Title: MSAalignment.py
# Project: ChowdhuryLab Datamining from website
# Description: Description
# Reference:
'''
TODO: write your reference here
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
import requests
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pyperclip as pc
import urllib3

#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def urlibb():
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://www.google.com/')
    print(r.data)

def request():
    resp = requests.post("https://www.google.com/", data = {"Search":"maplestory"})
    #resp.encoding = 'utf-8'
    print(resp)

def selenium():
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=op)
    driver.get("https://www.google.com/")

    search_input_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'
    search_input = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, search_input_xpath)))
    search_input.send_keys("maplestory")

    search_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]'
    element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    driver.execute_script("arguments[0].click();", element)

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

    print(str(driver.current_url))

    time.sleep(2)

    driver.close()
    driver.quit()

def hhblits():
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument('window-size=1920x1080')
    driver = webdriver.Remote(options=op)
    driver.get("https://toolkit.tuebingen.mpg.de/tools/muscle")

    # alignement
    alignment_xpath = '/html/body/div/div[1]/div[2]/div/div[3]/div[2]/div/nav/div/div/div/ul[1]/li[2]/a'
    alignment = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, alignment_xpath)))
    driver.execute_script("arguments[0].click();", alignment)

    # input box
    input_xpath = '/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[1]/div/div/div/div/div/fieldset/div/textarea'
    input = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, input_xpath)))
    str = ">1F6G_1|Chains A, B, C, D|VOLTAGE-GATED POTASSIUM CHANNEL|Streptomyces lividans (1916)\nGREQERRGHFVRFDRLERMLDDNRR\n>1J95_1|Chains A, B, C, D|VOLTAGE-GATED POTASSIUM CHANNEL|Streptomyces lividans (1916)\nMPPMLSGLLARLVKLLLGRHGSALHWRATLWGRCVAVVVMVALATWFVGREQERRGHF"
    input.send_keys(str)

    # example
    '''example_xpath = '/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[1]/div/div/div/div/div/fieldset/div/div[2]/button'
    example = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, example_xpath)))
    driver.execute_script("arguments[0].click();", example)'''

    # Submit
    time.sleep(0.5)
    submit_xpath = '/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[1]/fieldset/div/button/span'
    submit = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, submit_xpath)))
    driver.execute_script("arguments[0].click();", submit)

    # test change to msaprobs
    '''msaprobs_xpath = '/html/body/div/div[1]/div[2]/div/div[3]/div[2]/div/nav/div/div/div/ul[2]/li[5]/a'
    msaprobs = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, msaprobs_xpath)))
    driver.execute_script("arguments[0].click();", msaprobs)'''

    # two condition, exist the job, or does not.

    # new URL
    time.sleep(0.5)
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)


    if driver.current_url == "https://toolkit.tuebingen.mpg.de/tools/muscle":
        print("submission fail")
    print(driver.page_source)
    print(driver.current_url)  

    
    driver.close()
    driver.quit()


def main():
    urlibb()
    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<test_request>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<test_request>\" script --------------------\n")