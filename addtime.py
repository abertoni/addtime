#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("""
#############################
# # # # A D D T I M E # # # # 
#############################
""")

### Add time info to files with step info, using information located in a .log file
#### The .log file must have a header in the first line (where "Step" and "Time" columns are present) and the information below will be used for conversion of steps to times. Duplicated steps entries will be overwriten.
#### In the files to process the step column has to be present and a header is not required. The index of the column where step info is located has to be inputed as a the 'sinfo' variable. But, if the program fails to locate it, it will try to match the info in the other columns using the conversion dictionary (not recommended).
#### The user also has to add in 'filexs' (as elements in the list) the formats of the files that will be processed. Files with the "vs-t" tag will be ignored.

# Import modules
import numpy as np
import os
import sys

### USER DEFINED ###
# Possible extensions for files to process
# Add more without the dot (".")
filexs = ["txt","dat"]

# Column in file to process where Step info is located
# 0 corresponds to the first column in the file
sinfo = 0
# If it is not found, it will try with another one
####	####	####

### .LOG PROCESSING
# Selects the first .log file in alphabetic order
cwd = os.getcwd()
logfiles = [f for f in os.listdir(cwd) if f.endswith(".log")]
logfiles.sort()
try:
    logfile = logfiles[0]
    print(".log file found! (%s)"%logfile)
except:
    if len(logfiles)==0: print(".log file NOT found!")
    sys.exit()
        
# Read location of step and time columns
firstline = open(logfile,"r").readline()
firstcol = firstline.split()[0].strip()
if firstcol[0].isalpha():
    for idx,col in enumerate(firstline.split()):
        if col == "Step": idxstep = idx
        elif col == "Time": idxtime = idx
else:
    print("Header in first line NOT found!")
    sys.exit()
    
# Check if step and time info exists
try: 
    if idxstep != None and idxtime != None:
        print("Step and time info located!")
except:
    print("Step and time info not found in the .log file!")
    
# Build step to time conversion dictionary
convert = {}
logdata = np.genfromtxt(logfile)

nlines = logdata[:,0].size
for n in range(nlines):
    step = logdata[n,idxstep]
    time = logdata[n,idxtime]
    convert[step] = time

####	####	####

# FILE PROCESSING
files = [f for f in os.listdir(cwd) if f.split(".")[-1] in filexs and "vs-t" not in f]

for file in files:
    stepinfo = sinfo
    print("\nProcessing %s file..."%file)
    filedata = np.genfromtxt(file)
    nlines, ncols = filedata.shape
    newdata = np.zeros((nlines,ncols+1))

    # Check if step info is correct
    def checkinfo(): # Uses global varibles
        for n in range(nlines):
            step = filedata[n,stepinfo]
            try: convert[step]
            except: return False
        return True
            
    if not checkinfo():
        print("Step info not found where indicated...\n\t(Looking for an alternative)")
        for nc in range(ncols):
            stepinfo = nc
            if checkinfo(): 
                print("\t(Step info found in column index %s)"%stepinfo)
                break
            stepinfo = None
            
    if stepinfo == None:
        print("Step info not found at all!\nSkiping this file!\n")
        break
    
    for n in range(nlines):
        step = filedata[n,stepinfo]
        data = filedata[n,:]
        newdata[n,0] = convert[step]
        newdata[n,1:] = data
    np.savetxt(file.split(".")[0]+"-vs-t.dat",newdata,"%.4f")

####	####	####

print("\nAll done!")

print("\n~~~~~~~\nAndrés Ignacio Bertoni (andresibertoni@gmail.com) - 2019\n~~~~~~~")

################################################################################
# Andrés Ignacio Bertoni (andresibertoni@gmail.com) - 2019                     #
# Quantum Dynamics Group - Interdisciplinary Institute for Basic Science (ICB) #
# Faculty of Exact and Natural Sciences (FCEN)                                 #
# Cuyo National University (UNCuyo), Mendoza, Argentina.                       #
################################################################################
