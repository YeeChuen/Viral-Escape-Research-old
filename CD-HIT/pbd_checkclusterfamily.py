# Author/s: Yee Chuen Teh           (Author that contribute to the script)
# Title: pbd_checkclusterfamily.py          (the name of the script)
# Project: TODO: project title      (the main project name, what project this script is apart of?)
# Description: TODO: Description    (summary of what the script does)
# Reference:
'''
TODO: write your reference here
'''
# Updates:  (date)
'''
TODO: write your updates here
date
    - some update on this date
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here

#____________________________________________________________________________________________________
# functions/set ups 
    # TODO: write your functions here
def openfile(file):
    with open (file, 'r') as f:
        string = f.read()
        a_temp = string.split("\n")
        if a_temp[len(a_temp)-1] == "":
            a_temp.pop()
        return a_temp

def count_protein(a_list):
    count = 0
    max_counter = 0
    max = 0
    max_cluster = ""
    cluster_temp=""
    ge_10 = 0
    for a in a_list:
        if a[0] != ">":
            count+=1
            max_counter+=1
        else:
            if max_counter > max:
                max = max_counter
                max_cluster = cluster_temp
            if max_counter >= 10:
                ge_10 +=1
            max_counter=0
            cluster_temp = a
            continue
    if max_counter > max:
        max = max_counter
        max_cluster = cluster_temp
    
    print("Total protein clustered: {}".format(str(count)))
    print("number of cluster(family) with 10 or more proteins: {}".format(str(ge_10)))
    print("Cluster no. [{}] contain the most protein: {}".format(max_cluster, str(max)))

def main():
    # TODO: write your main here
    file = 'test_CD-HIT_1.clstr'
    a_temp = openfile(file)
    count_protein(a_temp)
    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    # TODO: change your python script title
    print("\n-------------------- START of \"<pbd_checkclusterfamily.py>\" script --------------------")
    main()
    print("-------------------- END of \"<pbd_checkclusterfamily.py>\" script --------------------\n")