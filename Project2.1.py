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
        and prints out the start and end time of the peaks.

        Technically I think this algorithm would generally find the peak widths correctly however
        the noise drifts upward throughout the run. """

    global time_t, absorb_t
    
    # Find all local minima and maxima
    local_max = argrelextrema(absorbance, numpy.greater)
    local_min = argrelextrema(absorbance, numpy.less)

    # If local minima surrounds peak maxima then that is the peak width
    min_time = []
    for x in peak_t:
        if x in time[local_max]:
            n = 1
            while n < len(time[local_min]):
                if time[local_min][n - 1] < x and time[local_min][n + 1] > x:
                    min_time.append(time[local_min][n])
                    n += 1
                else:
                    n += 1
        else:
            continue

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

    # Save the absorbance and time corresponding to the peak widths so they can be plotted later
    num = 0
    time_t = []
    absorb_t = []
    while num < len(time):
        if time[num] in min_time:
            time_t.append(time[num])
            absorb_t.append(absorbance[num])
            num += 1
        else:
            num += 1

    
def PlotPeaks(t, a, p_t, p_a, w_t, w_a):
    pyplot.plot(t, a)
    pyplot.plot(p_t, p_a, 'ro')
    pyplot.plot(w_t, w_a, 'gs')
    pyplot.show()


ReadFile(sys.argv[1])
PeakMax(time, corr_baseline)
PeakWidth(time, corr_baseline)
PlotPeaks(time, corr_baseline, peak_t, peak_a, time_t, absorb_t)
