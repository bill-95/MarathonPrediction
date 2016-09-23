
# coding: utf-8
#%matplotlib inline

import random, math
import csv, sys
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D


def generateTrainSet(features, degree):
    x = []
    for i in range(degree):
        x.append([pow(sample, i+1) for sample in features])
    x.append(np.ones(len(features)))
    trainingSet = np.array(x)
    return trainingSet

def findWeights(trainSetFeature, trainSetLabel, degree, L2Const=""):
    x = generateTrainSet(trainSetFeature, degree)
    x_t = np.transpose(x)
    y = np.array(trainSetLabel)
    XT_X = x.dot(x_t)
    XT_Y = x.dot(y).reshape(degree+1,1)
    w = inv(XT_X).dot(XT_Y)
    if L2Const != "":
        w = inv(XT_X + L2Const * np.transpose(w).dot(w)).dot(XT_Y)
    return w, x

def fittedLine(xVals, weights, degree):
    yVals = []
    for x in xVals:
        y = 0
        for i in range(degree):
            y = pow(x, i+1) * weights[i] + y
        y = y + weights[degree]
        yVals.extend(y)
    return yVals

def trainingError(dataSetFeature, dataSetLabel, weights):
    Xw = np.transpose(dataSetFeature).dot(weights)
    Xw = np.array([x[0] for x in Xw])
    a = list(np.array(dataSetLabel) - np.array(Xw))
    aT = np.transpose(a)
    error = aT.dot(a)/len(dataSetLabel)
    return error

def leaveOneOut(xVal, yVal, weights, degree):
    tempList = []
    tempList.append(xVal)
    predictedY = fittedLine(tempList, weights, degree)
    error = pow(yVal - predictedY[0], 2)
    return predictedY, error

def convertTime(time):
    timeList = str(time).split(".")
    hours = int(timeList[0])
    if hours < 10:
        hours = "0" + str(hours)
    minutesSeconds = str(float("0." + timeList[1])*60).split(".")
    minutes = int(minutesSeconds[0])
    if minutes < 10:
        minutes = "0" + str(minutes)
    seconds = int(float("0." + minutesSeconds[1])*60)
    if seconds < 10:
        seconds = "0" + str(seconds)
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)


################################################################


def main(dataFile, predictionFeatures, scaleFactors, degree):
    time = []
    fullX = []

    with open(predictionFeatures) as inFile:
        for i, row in enumerate(csv.reader(inFile)):
            if i == 0:
                continue
            else:
                if row[0] == "FULL":
                    fullX.append(float(row[1]))
                elif row[0] == "HALF":
                    fullX.append(float(row[1])*scaleFactors[0])
                elif row[0] == "TEN":
                    fullX.append(float(row[1])*scaleFactors[1])
                elif row[0] == "FIVE":
                    fullX.append(float(row[1])*scaleFactors[2])
                elif row[0] == "OTHER":
                    fullX.append(float(row[1])*scaleFactors[3])
                    
    with open(dataFile) as inFile:
        for i, row in enumerate(csv.reader(inFile)):
            if i == 0:
                continue
            else:
                if row[1] == "FULL":
                    time.append([float(row[2]), float(row[0])])
                elif row[1] == "HALF" or row[1] == "21.1 km":
                    time.append([float(row[2])*scaleFactors[0], float(row[0])])
                elif row[1] == "TEN" or row[1] == "10 km course":
                    time.append([float(row[2])*scaleFactors[1], float(row[0])])
                elif row[1] == "5 km" or row[1] == "FIVE":
                    time.append([float(row[2])*scaleFactors[2], float(row[0])])
                elif row[1] == "OTHER":
                    time.append([float(row[2])*scaleFactors[3], float(row[0])])

    
    random.shuffle(time)

    trainSetFeature = [sample[0] for sample in time]
    trainSetLabel = [sample[1] for sample in time]

    weightsList = []
    trainingErrorList = []
    validationErrorList = []
    actualDifference = []
    #Leave-One out cross validation
    for i in range(len(trainSetFeature)):
        newFeatureSet = [sample for j, sample in enumerate(trainSetFeature) if j != i]
        newLabelSet = [sample for j, sample in enumerate(trainSetLabel) if j != i]
        #train on all except i point
        w, x = findWeights(newFeatureSet, newLabelSet, degree)
        weightsList.append(w.tolist())
        trainError = trainingError(x, newLabelSet, w)
        trainingErrorList.append(trainError)
        #validate on i point
        predictedY, error = leaveOneOut(trainSetFeature[i], trainSetLabel[i], w, degree)
        validationErrorList.append(error)
        
    avgError = sum(trainingErrorList) / len(trainingErrorList)
    validationError = sum(validationErrorList) / len(validationErrorList)
    
    #find the average of the weights from training
    averageWeights = []
    for i in range(degree+1):
        averageWeight = sum([value[i][0] for j, value in enumerate(weightsList)])/len(weightsList)
        averageWeights.append([averageWeight])
    
    #calculate predicted values from full dataset
    predictedValList = []
    for i in range(len(fullX)):
        predictedY, error = leaveOneOut(fullX[i], fullX[i], np.array(averageWeights), degree)
        predictedValList.append(predictedY)
        
    #make the graph of the best fit curve and scatter plot for the training data
    x_axis = np.arange(0, 9, 0.01)
    y_axis = fittedLine(x_axis, np.array(averageWeights), degree)

    fig = pyplot.figure(figsize=(16,10))
    fig.suptitle('Most Recent Event Time vs. 2015 Full Marathon Time', fontsize=14, fontweight='bold')

    ax2 = fig.add_subplot(111)
    ax2.set_ylim([0, 9])
    ax2.set_xlim([0, 9])
    ax2.scatter(trainSetFeature, trainSetLabel)
    ax2.plot(x_axis, y_axis, color="red", linewidth=3)
    ax2.legend(['Fitted Curve', "Training Data"])
    ax2.set_xlabel('Most Recent Race Time (Scaled to Full Marathon) in Hours')
    ax2.set_ylabel('2015 Full Marathon Time in Hours')
    fig.show()

    return avgError, validationError, predictedValList

#######################################################################
if len(sys.argv)!=3:
    print("python linearRegression.py <Training_Data.csv> <Features_for_Prediction.csv>")
    sys.exit(0)

#scaling factors for each race catagory           
demi = 2.21428571429
ten = 7.11111111111
five = 10.2222222222
others = 4.0
degree = 4

#find training error and validation error and make predictions
fileToWrite = []
trainErrList = []
validErrList = []

trnErr, newValErr, fileToWrite = main(sys.argv[1], sys.argv[2], [demi, ten, five, others], degree)
#print(trnErr, newValErr)

#Writes out the predictions into a results.csv file
outFile = open("2016_Predictions.csv", "w")
writer = csv.writer(outFile)

for item in fileToWrite:
    if item[0] > 8:
        writer.writerow(["-1"])
    else:
        converted = convertTime(item[0])
        writer.writerow([converted])
        
outFile.close()
#print("done")


# In[ ]:




# In[ ]:




# In[ ]:



