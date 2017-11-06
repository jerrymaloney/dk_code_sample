# run with `python -c 'import dk; dk.methodName(params)'`
import re, sys
import collections

# probably removable before publication
import pprint
pp = pprint.PrettyPrinter(indent=2)

datastore='./latestSwing.csv'
verbose=False

"""
define the data structure as a list with two elements: the timestamp and a named tuple
[ [ timestamp,
    Measurement(
                  accelerometer_x_val=___,
                  accelerometer_y_val=___,
                  accelerometer_z_val=___,
                  gyroscope_x_val=___,
                  gyroscope_y_val=___,
                  gyroscope_z_val=___
               )
  ],
...
]
"""
Measurement = collections.namedtuple('Measurement', 'accelerometer_x_val, accelerometer_y_val, accelerometer_z_val, gyroscope_x_val, gyroscope_y_val, gyroscope_z_val')

def loadLines():
    l=[]
    data=open(datastore, 'r')
    for line in data:
        linelist=line.rstrip().split(',')
        timestamp=int(linelist[0])
        l.append([timestamp, Measurement(accelerometer_x_val=float(linelist[1]), accelerometer_y_val=float(linelist[2]), accelerometer_z_val=float(linelist[3]), gyroscope_x_val=float(linelist[4]), gyroscope_y_val=float(linelist[5]), gyroscope_z_val=float(linelist[6]))])
    return sorted(l)

def printLines():
    pp.pprint(loadLines())
    print len(loadLines())


def validateParameters(data, indexBegin, winLength):
    if data not in Measurement._fields:
        raise ValueError("%s is not a valid value for 'data'" % data)
    if indexBegin < 0:
        raise IndexError("indexBegin must be greater than or equal to 0")
    if winLength <= 0:
        raise IndexError("winLength must be greater than 0")
        
"""
from indexBegin to indexEnd, search data for values that are higher than threshold. Return the first index where data has values that meet this criteria for at least winLength samples

programmer's note: After initially trying just straight iteration, I thought it would be most efficient to reduce the size of the dataset for analysis as quickly as possible, then see if we can make a sequence out of it.
"""
def searchContinuityAboveValue(data, indexBegin, indexEnd, threshold, winLength):
    validateParameters(data, indexBegin, winLength)
    # validate parameters unique to this function
    if indexBegin > indexEnd:
        raise IndexError("indexBegin must be less than or equal to indexEnd")
    
    # find the set of measurements that meet the criteria, with their list indices
    measurements=loadLines()
    matchedMeasurements=[[measurements.index(measurement), measurement[0]] for measurement in measurements if getattr(measurement[1], data) > threshold]
    # eliminate unwanted indices from the comprehension
    limitedMeasurements=[matchedMeasurement for matchedMeasurement in matchedMeasurements if matchedMeasurement[1] >= indexBegin and matchedMeasurement[1] <= indexEnd]
    # iterate over the comprehension to find a sequence of length >= winLength
    for i in range(0, len(limitedMeasurements)-winLength+1):
        # If the index in the original matchedMeasurements list for the prospective last element of the sequence
        # is equal to the index in the original matchedMeasurements list for the first element PLUS winLength
        # then we have a sequence.
        # I wish I knew how to write that more clearly.
        if limitedMeasurements[i+winLength-1][0] == limitedMeasurements[i][0]+winLength-1:
            return limitedMeasurements[i][1]
    return None

"""
from indexBegin to indexEnd (where indexBegin is larger than indexEnd), search data for values that are higher than thresholdLo and lower than thresholdHi. Return the first index where data has values that meet this criteria for at least winLength samples.

programmer's note: I could do better at code re-use between the previous function and this one. There is a lot of overlap.
But re-using code would involve some variable name interpolation that would make the code harder to read.
"""
def backSearchContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    validateParameters(data, indexEnd, winLength)
    # validate parameters unique to this function
    if indexEnd > indexBegin:
        raise IndexError("indexEnd must be less than or equal to indexBegin")
    if thresholdHi is not None and thresholdLo > thresholdHi:
        raise ValueError("thresholdLo must be less than or equal to thresholdHi")
    
    # find the set of measurements that meet the criteria, with their list indices
    measurements=loadLines()
    matchedMeasurements=[[measurements.index(measurement), measurement[0]] for measurement in measurements if getattr(measurement[1], data) > thresholdLo and getattr(measurement[1], data) < thresholdHi]
    # eliminate unwanted indices from the comprehension
    limitedMeasurements=[matchedMeasurement for matchedMeasurement in matchedMeasurements if matchedMeasurement[1] >= indexEnd and matchedMeasurement[1] <= indexBegin]
    # iterate over the comprehension to find a sequence of length >= winLength
    if verbose: pp.pprint(limitedMeasurements)
    for i in range(len(limitedMeasurements)-1, winLength, -1):  # only go down to winLength because there is no possibility that a measurment after that will start a sequence long enough to match
        # If the index in the original matchedMeasurements list for the prospective last element of the sequence
        # is equal to the index in the original matchedMeasurements list for the first element PLUS winLength
        # then we have a sequence.
        # I wish I knew how to write that more clearly.
        if limitedMeasurements[i-winLength+1][0] == limitedMeasurements[i][0]-winLength+1:
            return limitedMeasurements[i][1]
    return None


"""
from indexBegin to indexEnd, search data1 for values that are higher than threshold1 and also search data2 for values that are higher than threshold2. Return the first index where both data1 and data2 have values that meet these criteria for at least winLength samples.
"""
def searchContinuityAboveValueTwoSignals(data1, data2, indexBegin, indexEnd, threshold1, threshold2, winLength):
    raise NotImplemetedError()

"""
from indexBegin to indexEnd, search data for values that are higher than thresholdLo and lower than thresholdHi. Return the the starting index and ending index of all continuous samples that meet this criteria for at least winLength data points.
"""
def searchMultiContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    raise NotImplemetedError()
