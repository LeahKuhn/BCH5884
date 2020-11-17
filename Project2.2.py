#!/usr/bin/env python3
#github.com/LeahKuhn/BCH5884

import sys, numpy
from matplotlib import pyplot
from scipy.signal import argrelextrema


def ReadFile(filename):
    """ Read input file and extra the time and absorbance data into arrays.  Then correct the baseline
        down to 0 using a linear assumption for first and last data point """
    
    global time, corr_baseline
    f = open(filename)
    lines = f.readlines()
    
    f.close()

    time = []
    absorb = []
    
    for line in lines[3:]:
        words = line.split()
        try:
            time.append(float(words[0]))
            absorb.append(float(words[1]))
        except:
            #print("Could not parse.", line)
            continue
    
    time = numpy.array(time)
    absorb = numpy.array(absorb)

    # Correct baseline, assuming baseline is linear between first and last data point
    corr = (absorb[0] + absorb[-1])/2
    corr_baseline = []
    for x in absorb:
        corr_baseline.append(x-corr)

    corr_baseline = numpy.array(corr_baseline)
    
    """
    pyplot.plot(time,corr_baseline)
    pyplot.plot(time,absorb)
    pyplot.show()
    """
    

def PeakMax(time, absorbance):
    """ Determines the peaks with a height of greater than 10"""
    
    global peak_t, peak_a
    
    # Read through corr_baseline array
    # Point is a peak if x is larger than neighbors
    # Make list of peak absorbance and corresponding time
    peak_a = []
    peak_t = []
    n = 1
    while n < (len(absorbance) - 1):
        if absorbance[n - 1] < absorbance[n] and absorbance[n + 1] < absorbance[n] and absorbance[n] > 10:
            #print("Peak Found:", absorbance[n], time[n])
            peak_a.append(absorbance[n])
            peak_t.append(time[n])
            n += 1
        else:
            n += 1

    # Print output to user
    x = 0
    print(len(peak_a), "Peaks Found")
    while x < len(peak_a):
        peak_num = x + 1
        output = "Peak {:d} Time: {:.3f} Absorbance: {:.3f}"
        print(output.format(peak_num, peak_t[x], peak_a[x]))
        x += 1


    
    

def PeakWidth(time, absorbance):
    """ Determine peak start and end time by looking for minima surrounding the identified peak
        and prints out the start and end time of the peaks"""

    da = numpy.gradient(absorbance)
    slopes = numpy.array(da)
    change = 0
    x1 = []
    x2 = []
    y1 = []
    y2 = []
    coord1 = []
    coord2 = []

    for i in range(len(slopes)):
        if slopes[i]>change:
            x1.append(time[i])
            y1.append(absorbance[i])
            coord1.append((time[i],absorbance[i]))
        elif slopes[i]<change:
            x2.append(time[i])
            y2.append(absorbance[i])
            coord2.append((time[i],absorbance[i]))
    #print(coord1)
    print(coord2)
            
            
    """
    # Print output to user
    x = 0
    n = 0
    print("\nPeak start and end times")
    while x < len(min_time):
        peak_num = n + 1
        output = "Peak {:d} Start: {:.3f} End: {:.3f}"
        print(output.format(peak_num, min_time[x], min_time[x+1]))
        n += 1
        x += 2
    """


    
def PlotPeaks(t, a, p_t, p_a, w_t, w_a):


    pyplot.plot(t, a)
    pyplot.plot(p_t, p_a, 'ro')
    pyplot.plot(w_t, w_a, 'gs')
    pyplot.show()


ReadFile(sys.argv[1])
PeakMax(time, corr_baseline)
PeakWidth(time, corr_baseline)
PlotPeaks(time, corr_baseline, peak_t, peak_a, time_t, absorb_t)
