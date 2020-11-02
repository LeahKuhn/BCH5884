#!/usr/bin/env python3
#https://github.com/LeahKuhn/BCH5884

import sys, math
from decimal import Decimal

def readfiles(file1, file2):
    """
    loop that takes first file and reads out the input then repeats with
    second file
    """
    global tmplist1, tmplist2

    
    # Open file1.pdb from user input
          
    #filetmp=file1
    f=open(file1,'r')
    lines=f.readlines()

    # Save rows of pdb file to lists
    tmplist1=[]
    for line in lines:
        words=line.split()
        words[1]=(int(words[1]))
        words[5]=(int(words[5]))

        for i in range (6, (len(words)-1)):
            words[i] = Decimal(words[i])
         
        tmplist1.append(words)
    
    f.close()
        

    # open file2.pdb and put into lists
    f=open(file2,'r')
    lines=f.readlines()

    # Save rows of pdb file to lists
    tmplist2=[]
    for line in lines:
        words=line.split()
        if len(words) != 12:
            pass
        
        else:
            words[1]=(int(words[1]))
            words[5]=(int(words[5]))
    
            for i in range (6, (len(words)-1)):
                words[i] = Decimal(words[i])
        
            tmplist2.append(words)
    f.close()
    #sys.exit()
        
def rmsd(data1, data2):
    """*************************************************
    Determines the root-mean-square deviation for two
    .pdb files that are being stored in lists and prints
    out the root-mean-square deviation value
    *************************************************"""
    sum_coor = 0
    for x in range(0, len(data1)):
        # find difference then square for x, y, and z coordinates
        x_diff_sqr = (data1[x][6] - data2[x][6])**2
        y_diff_sqr = (data1[x][7] - data2[x][7])**2
        z_diff_sqr = (data1[x][8] - data2[x][8])**2
        
        sum_coor = sum_coor + x_diff_sqr + y_diff_sqr + z_diff_sqr
        
    # Determine root-mean-square using sum from above and the length of the list
    rmsd_value = math.sqrt(sum_coor/len(data1))
    print("Root-mean-square deviation:", rmsd_value)


        
if __name__ == "__main__":
    readfiles(sys.argv[1], sys.argv[2])
    rmsd(tmplist1, tmplist2)
