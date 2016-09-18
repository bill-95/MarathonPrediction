# will group the types output from type_scrub.py in to 1 row for each type
# this is to generate a list to be used on the main data set

# takes 2 command line arguments, input file and output file

import sys
import csv

# open the file and read the 
with open(sys.argv[1], 'rb') as input_csvfile:
	reader = csv.reader(input_csvfile)
	data = list(reader)

grouped = []
grouped.append(["FULL"])
grouped.append(["HALF"])
grouped.append(["TEN"])
grouped.append(["FIVE"])
grouped.append(["OTHER"])

for i in range(0, len(data)):
	if data[i][1] == "FULL":
		grouped[0].append(data[i][0])
	elif data[i][1] == "HALF":
		grouped[1].append(data[i][0])
	elif data[i][1] == "TEN":
		grouped[2].append(data[i][0])
	elif data[i][1] == "FIVE":
		grouped[3].append(data[i][0])
	elif data[i][1] == "OTHER":
		grouped[4].append(data[i][0])

# write back to a new file
with open(sys.argv[2], 'wb') as output_csvfile:
	writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

	# write each row in the csv file
	for i in grouped:
		writer.writerow(i)