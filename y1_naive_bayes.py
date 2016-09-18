# 1st argv index is the input file name, 2nd is the output file name

import numpy
import scipy
import sklearn
import csv
import sys

# open the file and read the 
with open(sys.argv[1], 'rb') as input_csvfile:
	reader = csv.reader(input_csvfile)
	data = list(reader)

# insert column headers for number of races and wheter they ran in 2014
data[0].insert(1,"NUM_FULL")
data[0].insert(2, "NUM_HALF")
data[0].insert(3, "NUM_10")
data[0].insert(4, "NUM_5")

row_length = len(data[0])

# iterate through each item in data that isn't the header row
for i in range(1,len(data)):
	for j in range(3, len(data[i]), 5):
		if "Demi" in


# write back to a new file
with open(sys.argv[2], 'wb') as output_csvfile:
	writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

	# write each row in the csv file
	for i in data:
		writer.writerow(i)

		
