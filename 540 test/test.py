# Author: Yee Chuen Teoh
# Title: COM S 540 Part 0

#________________________________________________
# imports
import argparse
import os.path
import sys
from Source.part_1 import *

#________________________________________________
# functions

def main():
        arg = sys.argv
        if len(arg) == 1:
                standard_error()
        else:
                arg_mode = arg[1]
                mode = arg_mode[1:]
                if mode == "0" or mode == "v":
                        standard_output()

                elif mode == "1":
                        part_1.main()

                else:
                        print("")
                        print("Error in argument.")
                        print("argument \"{}\" unavailable.".format(str(arg_mode)))
                        standard_error()

def standard_output():
        print("")
        print("=================================================================================")
        print("|\tYee's bare-bones Python compiler (for COM 440/540)\t\t\t|")
        print("|\t\tWritten by Yee Chuen Teoh (chuen@iastate.edu)\t\t\t|")
        print("|\t\tVersion 1.0, updated as of 10:51pm 24th  January 2023\t\t|")
        print("=================================================================================")
        print("")

def standard_error():
        print(" ______________________________________________________________________ ")
        print("+                                                                      +")
        print("mycc is a python compiler project for COM S 440/540.")
        print("")
        print("   Usage:")
        print("\tmycc -mode [infile]")
        print("")
        print("   Valid mode:")
        print("\t-0:\t Version information only")
        print("\t-1:\t Part 1 (not yet implemented)")
        print("")
        print("   Optional Argument:")
        print("\t-v:\t Version information only (similar to \"-0\"")
        print("+______________________________________________________________________+")


#________________________________________________
# main

if __name__ == "__main__":
        main()
