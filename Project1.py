#!/usr/bin/env python3
#Leah Kuhn

import sys
from decimal import Decimal

"""
*******************************************************************************************************************
Project1.py <file.pdb> <filename.out>

Usage: In order to use this code you need to provide a .pdb file and give a .out file to save the information from
the .pdb file in.

Job: This code will open the .pdb file and save the row data as a list of lists.  The code will then append the mass
of the atom to the list.  Once this is completed the formatted output file will be generated.  Afterwards the code
will ask the user if they want to calculate geometric center [0] or center of mass [1].  Depending on user input
the code will calculate one or the other and print the coordinates for the user. If a invalid number is entered (not
0 or 1) the code will tell the user to input either 0 or 1.
*****************************************************************************************************************
"""

if len(sys.argv) != 3:
    print("Usage: Project1.py <file.pdb> <filename.out>")
    print("____________________________________________")
    sys.exit()

# Open file.pdb from user input
readfile=sys.argv[1]
f=open(readfile,'r')
lines=f.readlines()

# Save rows of pdb file to lists
tmplist=[]
for line in lines:
    words=line.split()
    words[1]=(int(words[1]))
    words[5]=(int(words[5]))
    
    for i in range (6, (len(words)-1)):
        words[i] = Decimal(words[i])
        
    tmplist.append(words)

    # Get mass from atom and add it to the end of list of atom data
    if words[11] == "N":
        words.append(14)
    if words[11] == "C":
        words.append(12)
    if words[11] == "O":
        words.append(16)
    if words[11] == "S":
        words.append(32)
    
f.close()
#sys.exit()

#user_in=input("Insert name for output file as 'filename.out':  ")

# Format new .pdb file
f=open(sys.argv[2], 'w')
for tmp in tmplist:
    sent="{:6}{:>5d} {:4} {:3} {}{:>4} {:>11.3f}{:>-8.3f}{:>8.3f}{:6.2f}{:6.2f}{:>12}\n"
    f.write(sent.format(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11]))
f.close()

print("Data from .pdb file saved to:", sys.argv[2])
print("          ____________________          ")
    

# Get user input for geometric center or center of mass
center=int(input("\nCalculate geometric center [0] or center of mass [1]?  "))


# Determine center of mass
if center == 1:
    sum_x = 0
    sum_y = 0
    sum_z = 0
    mass = 0

    for x in range(0, len(tmplist)):
        # sum(mass*x_coordinate)
        x_individ=tmplist[x][12] + tmplist[x][6]
        sum_x = sum_x + x_individ
        # sum(mass*y_coordinate)
        y_individ=tmplist[x][12] + tmplist[x][7]
        sum_y = sum_y + y_individ
        # sum(mass*z_coordinate)
        z_individ=tmplist[x][12] + tmplist[x][8]
        sum_z = sum_z + z_individ
        # sum of mass
        mass = mass + tmplist[x][12]

    # Center of mass = Sum(m*r)/sum(m)
    x_coor = sum_x / mass
    y_coor = sum_y / mass
    z_coor = sum_z / mass

    # Print output to user
    output="Center of mass coordinates: ({:.2f}, {:.2f}, {:.2f})"
    print(output.format(x_coor, y_coor, z_coor))

  
    

# Determine geometric center -> mean position of all points in all the coordinate directions    
elif center == 0:
    x_sum = 0
    y_sum = 0
    z_sum = 0
    
    for x in range(0, len(tmplist)):
        x_i=tmplist[x][6]
        x_sum = x_sum + x_i

        y_i=tmplist[x][7]
        y_sum = y_sum + y_i

        z_i=tmplist[x][8]
        z_sum = z_sum + z_i

    # geometric center = sum of coordinates / number of coordiantes
    x_avg = x_sum / (len(tmplist) + 1)
    y_avg = y_sum / (len(tmplist) + 1)
    z_avg = z_sum / (len(tmplist) + 1)

    # Print output to user
    output = "Geometric center coordinates: ({:.2f}, {:.2f}, {:.2f})"
    print(output.format(x_avg, y_avg, z_avg))

# Give user error because did not follow directions   
else:
    print("Invalid input. Please enter either 0 or 1")




