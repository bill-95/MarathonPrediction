# Jacob Charles
# COMP551
# A naive bayes classifier for predicting whether or not individuals will participate in the 2016 Oasis Montreal Marathon

# 1st argv index is the input file name, 2nd is the output file name

# input file should be as follows:
# ID | PRESENT2015 | PRESENT2014 | PRESENT2013 | PRESENT2012 | NUMOASIS
# 01 |     0       |     1       |     1       |     0       |     3    
# ..........

# The PRESENT20XX features are binary with 1 representing they were present at the 20XX marathon and 0 representing they were not present
# the NUMOASIS feature is the total number of oasis events the person has participated in including events smaller in distance
# than the full montreal marathon

import math
import csv
import sys
import time

# open the csv file
def openCSV():

	# open the file and read the input data
	with open(sys.argv[1], 'rb') as input_csvfile:
		reader = csv.reader(input_csvfile)
		data = list(reader)

	data = data[1:] # remove the header list entry

	return data


# will separate the training data by class value for statistical calculation purposes
def classSort(data):

	yes = [] # for rows where they attended the 2015 marathon
	no = [] # for rows where they did not attend the 2015 marathon

	for i in range(len(data)):
		if data[i][1] == "0":
			no.append(data[i])
		elif data[i][1] == "1":
			yes.append(data[i])

	return [yes, no]


# takes in the data and transposes it
# this is for calculating statistics on the data
def transpose(data):

	temp = [[],[],[]] # transpose is only used for the three binary features

	for i in range(len(data)):
		for j in range(len(temp)):
			temp[j].append(float(data[i][j+2]))

	return temp


# calculate P(y = yes, no)
def yesNoProbability(data):
	
	yes_count = 0.0
	no_count = 0.0

	for i in range(len(data)):
		if data[i][1] == "1":
			yes_count += 1.0 # count the number of yes
		elif data[i][1] == "0":
			no_count += 1.0 # count the number of nos

	return [yes_count / len(data), no_count / len(data)] 


# calculate the probability for a bernoulli feature
def bernoulliProbabiity(data):
	temp = 0.0

	for i in range(len(data)):
		if data[i] == 1.0:
			temp += 1 # count the number of times 1.0(yes) comes up

	return (temp / len(data))


# calculate the bernoulli probability across all of the binary features
def bernoulliProbabilities(data):
	 temp = transpose(data)
	 bernoullis = []
	 for i in range(len(temp)):
	 	bernoullis.append(bernoulliProbabiity(temp[i]))

	 return bernoullis


# calculate the mean of a list
def mean(data):
	
	temp = 0.0

	for i in range(len(data)):
		temp += float(data[i])

	return temp / len(data)


# calculate the standard deviation for an input list
def stdev(data):

	average = mean(data)
	temp = data[:]

	for i in range(len(data)):
		temp[i] = math.pow((float(data[i])-average), 2)

	return math.sqrt(sum(temp) / (len(data) - 1))


# gaussian function for an input value, mean of the feature, and stdev of the feature 
def gaussProbDensity(value, mean, stdev):
	exponent = math.exp(-(math.pow(value-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent 


# calculate the probability for a testing data given training data
# note that testing_data should be one row of the overall data without id or 2015 removed
def classProbability(training_data, testing_data):

	yes_prob, no_prob = yesNoProbability(training_data) # get P(y) for each class 

	yes_data, no_data = classSort(training_data) # split training data in to yes and no classes

	yes_bernoullis = bernoulliProbabilities(yes_data) # get the bernoulli probability for yes
	no_bernoullis = bernoulliProbabilities(no_data)  # get the bernoulli probability for no

	# generate the list for numoasis to calculate p(numoasis = x | yes)
	yes_oasis_list = []
	for i in range(len(yes_data)):
		yes_oasis_list.append(yes_data[i][5])

	# generate the list for numoasis to calculate p(numoasis = x | no)
	no_oasis_list = []
	for i in range(len(no_data)):
		no_oasis_list.append(no_data[i][5])

	# calculate the means for number of oasis events given yes and no
	yes_mean = mean(yes_oasis_list) 
	no_mean = mean(no_oasis_list)

	# calculate the stdevs for the number of oasis events given yes and no
	yes_stdev = stdev(yes_oasis_list)
	no_stdev = stdev(no_oasis_list)

	# set the conditional probabilities to be multiplied
	yes_cond_prob = 1
	no_cond_prob = 1

	# calculate the yes conditional probability
	for i in range(len(yes_bernoullis)):
		if testing_data[i+2] == "1":
			yes_cond_prob *= yes_bernoullis[i]
		elif testing_data[i+2] == "0":
			no_cond_prob *= (1.0-yes_bernoullis[i])

	# calculate the no conditional probability
	for i in range(len(no_bernoullis)):
		if testing_data[i+2] == "1":
			yes_cond_prob *= no_bernoullis[i]
		elif testing_data[i+2] == "0":
			no_cond_prob *= (1.0-no_bernoullis[i])

	yes_cond_prob *= yes_prob # multiply by P(y=yes)
	no_cond_prob *= no_prob # multiply by P(y=no)

	yes_cond_prob *= gaussProbDensity(float(testing_data[5]), yes_mean, yes_stdev) # multiply by p(numoasis = x | yes)

	no_cond_prob *= gaussProbDensity(float(testing_data[5]), no_mean, no_stdev) # # multiply by p(numoasis = x | no)

	return [yes_cond_prob, no_cond_prob]


# the predictor function
def prediction(training_data, testing_data):

	probabilities = classProbability(training_data, testing_data)

	if probabilities[0] > probabilities[1]:
		return "1"
	elif probabilities[1] > probabilities[0]:
		return "0"


# leave one out cross validation
def loocv(data):

	results = []

	for i in range(0, len(data)):
		temp = data[i] # store the values for the validation row
		data.pop(i) # remove the row from the data
		results.append(prediction(data, temp)) # run the prediction
		data.insert(i, temp) # reinsert the value

		print '\r', i, "of", len(data), 
		sys.stdout.flush()

	return results


# write out the results to a csv with filename contained in argv[2]
def writeCSV(data):
	with open(sys.argv[2], 'wb') as output_csvfile:
		writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

		# write each row in the csv file
		for i in data:
			writer.writerow(i)


def main():

	data = openCSV() # open the csv file
			
	results = loocv(data) # call leave one out on the data

	hits = 0.0 # number of hits for accuracy

	# initialize the count variables
	truepos = 0.0
	trueneg = 0.0
	falsepos = 0.0
	falseneg = 0.0

	for i in range(len(results)):
		if data[i][1] == results[1]:
			hits += 1
		if data[i][1] == "1" and results[i] == "1":
			truepos += 1
		if data[i][1] == "1" and results[i] == "0":
			falseneg += 1
		if data[i][1] == "0" and results[i] == "1":
			falsepos += 1
		if data[i][1] == "0" and results[i] == "0":
			trueneg += 1

	print "\nError:", (falsepos+falseneg) / (falsepos + falseneg + truepos + trueneg)
	print "Accuracy:", (1 -  (falsepos+falseneg) / (falsepos + falseneg + truepos + trueneg))

	print "True positive:", (truepos / len(results) * 100), "%", truepos
	print "True negative:", (trueneg / len(results) * 100), "%", trueneg
	print "False positive:", (falsepos / len(results) * 100), "%", falsepos
	print "False negative:", (falseneg / len(results) * 100), "%", falseneg

	writeCSV(results) # write the results

main()