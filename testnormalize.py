import math
from pbd_checkdash import *
from pbd_length import *

def normalize():
    target = 80
    norm = math.floor(target/100)
    condense = True
    n_index = 0
    counter = -1
    percent = 1
    for i in range(target):
                print("iter {}".format(str(i)))
                print("counter: {}".format(str(counter)))
                if condense == True:
                    if (target)%(100) == n_index:
                        condense = False
                        counter = 0

                if counter+1 == norm or i == target-1:
                    print("load into percentile: {}".format(str(percent)))
                    if condense == True:
                        counter = -1
                    else:
                        counter = 0
                    percent+=1
                    n_index+=1
                else:
                    counter +=1


def main():
    seq = "MDKE-----------------------------------EVK-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------REMKEQEGNPEVKSKRREVHMEILSEQVKSDIENSRLIVAN--sdflk--"
    test_split = split_alph_dash(seq)
    print("alphabet: {}".format(str(test_split[0])))
    print("dashes: {}".format(str(test_split[1])))

    path = "PoreDB_test/plottest.fas"
    a_temp = fas_to_list(path)
    b_temp = split_des_seq(a_temp)
    print(b_temp)
    name_list = extract_name(a_temp)
    seq_list = b_temp[1]
    plot_2d(seq_list, name_list[0], name_list[1])

    pass

if __name__ == "__main__":
    main()