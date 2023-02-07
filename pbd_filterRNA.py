# Author/s: Yee Chuen Teh
# Title: pbd_filerRNA.py
# Project: Chowdhury Lab Viral Escape
# Description: TODO: Description
# Reference:
'''
TODO: write your reference here
'''
'''
TODO:
- add argument in, input file and output file.
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
import argparse
import os
import sys

#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def readfas(file):
    with open (file, 'r') as f:
        s = f.read()
        s_list = s.split("\n")
        if s_list[len(s_list)-1] == "":
            s_list.pop()
        return s_list

def checkRNA(seq):
    RNA = ["A","U","G","C"]
    for letter in seq:
        if letter not in RNA:
            return False
    return True

def removeRNA(f_list):
    a = []
    for i in range(0,len(f_list),2):
        if f_list[i] == "":
            continue
        if checkRNA(f_list[i+1]) == False:
            a.append(f_list[i])
            a.append(f_list[i+1])
    return a
    

def save(non_RNA, i_file, o_file):
    isExist = os.path.exists(o_file)
    if not isExist:
        os.mkdir(o_file)
    path = os.getcwd()
    save_path = path +"/"+o_file
    os.chdir(save_path)

    global name
    if "." in i_file:
        name = i_file.split(".")
    else:
        name.append(i_file)
    with open("{}_nonRNA.fas".format(name[0]), 'a') as f:
        for p in non_RNA:
            f.write(p + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', type=str, required=True)
    parser.add_argument('--o', type=str, required=True)
    args = parser.parse_args()

    o_file = args.o
    file = args.i
    f_list = readfas(file)
    non_RNA = removeRNA(f_list)
    i_file = file.split("/")
    save(non_RNA, i_file[1], o_file)
    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"pbd_filerRNA.py\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"pbd_filerRNA.py\" script --------------------\n")