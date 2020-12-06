#!/usr/bin/env python3
#github.com/LeahKuhn/BCH5884

import sys, numpy, re
import matplotlib.pyplot as plt
#import webbrowser


def ReadFile_IR(filename):
    
    """****************************************************************
    Input: file.log
    Output: frequency, intensity

    Read the input .log file and parse the frequency and IR intensity
    using regular expressions.  Then return the frequency and intensity
    as two lists of floats.
    ****************************************************************"""
    
    f = open(filename)
    lines = f.readlines()
    f.close()

    freq_hold = []
    intensity_hold = []
    
    # Keep lines that start with frequency or IR intensity
    for line in lines:
        if line.startswith(' Frequencies'):
            freq_hold.append(line)
        elif line.startswith(' IR'):
            intensity_hold.append(line)

    freq = []
    intensity = []

    # Keep just the frequency and intensity values and ignore the rest of the line
    for x in freq_hold:
        match = re.findall('\d+\W\d+', x)
        for y in match:
            freq.append(float(y))

    for x in intensity_hold:
        match = re.findall('\d+\W\d+', x)
        for y in match:
            intensity.append(float(y))

    #print(freq)
    #print(intensity)

    return(freq, intensity)

    
def ReadFile_Thermo(filename):

    """*****************************************************
    Input: file.log
    Output: energy, enthalpy, and gibbs

    Read the input .log file and use regular expressions to
    find the energy, enthalpy, and gibb's free energy.  Then
    return the three values as floats.
    *****************************************************"""
    
    f = open(filename)
    lines = f.readlines()
    f.close()

    energy_hold = []
    enthalpy_hold = []
    gibbs_hold = []

    # Find lines containing data
    for line in lines:
        if 'thermal Energies' in line:
            energy_hold.append(line)
        elif 'thermal Enthalpies' in line:
            enthalpy_hold.append(line)
        elif 'thermal Free' in line:
            gibbs_hold.append(line)

    # Keep only the data values
    for x in energy_hold:
        match = re.findall('\d+\W\d+', x)
        for y in match:
            energy = (float(y))

    for x in enthalpy_hold:
        match = re.findall('\d+\W\d+', x)
        for y in match:
            enthalpy = (float(y))
            
    for x in gibbs_hold:
        match = re.findall('\d+\W\d+', x)
        for y in match:
            gibbs = (float(y))

    return(energy, enthalpy, gibbs)

def calcEnergy(E1, E2):

    """*****************************************************
    Input: Two energy values where E1 is initial and E2
        is final.
    Output: Returns the change in energy
    *****************************************************"""
    
    dE = E2 - E1
    return(dE)

def calcEnthalpy(H1, H2):
    
    """*****************************************************
    Input: Two enthalpy values where H1 is initial and H2
        is final.
    Output: Returns the change in enthalpy
    *****************************************************"""
    
    dH = H2 - H1
    return(dH)

def calcGibbs(G1, G2):
    
    """*****************************************************
    Input: Two Gibb's free energy values where G1 is initial
        and G2 is final.
    Output: Returns the change in Gibb's
    *****************************************************"""
    
    dG = G2 - G1
    return(dG)

def convertKcM(value):
    
    """******************************************************
    Input: value in a.u.
    Output: value converted to kcal/mol

    Converts a value in a.u. to kcal/mol
    ******************************************************"""
    
    newvalue = value * 627.5
    return(newvalue)

def PlotIR(frequency_1, IR_intensity_1, frequency_2, IR_intensity_2, intensity_value):

    """*****************************************************
    Input: The frequency and IR intensity as individual
        lists for the two IR spectra to compare.
    Output: Plot of the two IR spectra

    Plots two IR spectra and gives the frequency of the peaks
    with a greater intensity than the intensity specified
    by the user.
    *****************************************************"""

    
    plt.figure(figsize=(10.0,7.0))
    plt.subplot(211)

    # Make stem plot
    plt.stem(frequency_1, IR_intensity_1, 'b', markerfmt=' ', basefmt='b')
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.title(sys.argv[1])

    # Hide axes of first plot
    plt.gca().axes.yaxis.set_visible(False)
    plt.gca().axes.xaxis.set_visible(False)

    # Label peaks with intensity greater than intensity value
    for x,y in zip(frequency_1,IR_intensity_1):
        if y > intensity_value:
            label = '{:.2f}'.format(x)
            plt.annotate(label, (x,y))
    
    plt.subplot(212)
    plt.stem(frequency_2, IR_intensity_2, 'r', markerfmt=' ', basefmt='r')
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.xlabel('Frequency $(cm^{-1})$')
    plt.title(sys.argv[2])
    plt.gca().axes.yaxis.set_visible(False)


    for x,y in zip(frequency_2,IR_intensity_2):
        if y > intensity_value:
            label = '{:.2f}'.format(x)
            plt.annotate(label, (x,y))
            
    # Save image to put into HTML
    plt.savefig("IRcompare.png", orientation='landscape')       
    #plt.show()


def writeHTMLhead():
    
    """********************************************
    Write the intro lines for HTML code
    *******************************************"""

    message = """
<!DOCTYPE html>
<html>
    <head>
        <title> Final Project </title>
        <style>
        div {
            font-family:Arial, sans-serif;
        }
        h3 {
            text-align:center;
        }
        .img-container {
            text-align: center;
        }
        </style>
    </head>

    <body>
    
"""

    return(message)

def imageHTML(message):

    """****************************************
    Input plot image into HTML file
    ****************************************"""
    
    message2 = message + """

    <div class="img-container">
        <h1 style=text-align:center;>Computational IR</h1>
        <img src="IRcompare.png">
    </div>
"""
    return(message2)

def thermoHTML(file1, file2, e1, h1, g1, e2, h2, g2, dE, dH, dG, message):

    """***************************************
    Add thermodynamics data to HTML file
    ***************************************"""

    addmessage = """

    <div>
        <h1 style=text-align:center;>Thermodynamics</h1>
        <p>Initial: {:s} </p>
        <p>Energy: {:.2f} a.u. </p>
        <p>Enthalpy: {:.2f} a.u. </p>
        <p>Gibb's: {:.2f} a.u. </p>
        <br>

        <p>Final: {:s}</p>
        <p>Energy: {:.2f} a.u. </p>
        <p>Enthalpy: {:.2f} a.u. </p>
        <p>Gibb's: {:.2f} a.u. </p>
        <br>

        <p>Final - Initial</p>
        <p>dE: {:.2f} kcal/mol </p>
        <p>dH: {:.2f} kcal/mol </p>
        <p>dG: {:.2f} kcal/mol </p>
    </div>
"""
    message2 = message + addmessage.format(file1, e1, h1, g1, file2, e2, h2, g2, dE, dH, dG)
    
    return(message2)


def generateHTML(fileOut, message):
    
    """*****************************************************
    Input: Name of .html from user input and the string
        of html text
    Output: None

    Generate the .html file and write to the file using the
    message string generated
    *****************************************************"""
    
    filename = fileOut + '.html'
    f = open(filename, 'w')
    
    f.write(message)
    f.close()

    #webbrowser.open_new_tab('fileOut.html')


#***************** End of Functions **************************

# Read two input files then plot IR
f, i = ReadFile_IR(sys.argv[1])
f2, i2 = ReadFile_IR(sys.argv[2])
PlotIR(f, i, f2, i2, 50)

# Parse thermodynamics for two input files
e1, h1, g1 = ReadFile_Thermo(sys.argv[1])
e2, h2, g2 = ReadFile_Thermo(sys.argv[2])

# Calculate thermodynamics between the two files
DG = calcGibbs(g1, g2)
DE = calcEnergy(e1, e2)
DH = calcEnthalpy(h1, h2)

# Convert from a.u. to kcal/mol
dG = convertKcM(DG)
dE = convertKcM(DE)
dH = convertKcM(DH)

# Create HTML file
head = writeHTMLhead()
image = imageHTML(head)
message = thermoHTML(sys.argv[1], sys.argv[2], e1, h1, g1, e2, h2, g2, dE, dH, dG, image)
generateHTML(sys.argv[3], message)

