# 1st argv index is the input file name, 2nd is the output file name
# takes in a list of all race types given in the original data and will assign a tag for easy readability 
# if a type isn't caught by the list of strings the user will manually input the tag

import numpy
import scipy
import sklearn
import csv
import sys

# open the file and read the 
with open(sys.argv[1], 'rb') as input_csvfile:
	reader = csv.reader(input_csvfile)
	data = list(reader)

half = ("Demi", "demi", "Half", "half", "Half-", "21 km", "21 k", "21km", "21", "21k", "20", "21.1km")
ten = ("10 KM", "10 K", "10KM", "10K", "10 k", "10km", "10k", "10 km")
five = ("5 k", "5km", "5k", "5 km", "5 K", "5 KM", "5KM", "5k")
other = ("1 km", "1 KM", "1 k", "1 K", "1km", "1k", "1 km", "1 k", "triathlon", "fondo", "Fondo", "Triathlon",
	"duathlon", "Duathlon", "sprint", "skate", "Skate", "Patin", "patin", "Mud", "mud", "25km", "Triathon", "25 km", "25 Km", "uthc28", "uthc80")
full = ("marathon", "Marathon", "full", "Full")

try:
	# iterate through each item in data that isn't the header row
	for i in range(0,len(data)):
		if any(s in str(data[i]) for s in half) and len(data[i]) is 1:
			data[i].insert(1, "HALF")
		elif any(s in str(data[i]) for s in other) and len(data[i]) is 1:
			data[i].insert(1, "OTHER")
		elif any(s in str(data[i]) for s in ten) and len(data[i]) is 1:
			data[i].insert(1, "TEN")
		elif any(s in str(data[i]) for s in five) and len(data[i]) is 1:
			data[i].insert(1, "FIVE")
		elif any(s in str(data[i]) for s in full) and len(data[i]) is 1:
			data[i].insert(1, "FULL")
		elif len(data[i]) is 1:
			print data[i]
			print i, "of", len(data) 
			data[i].insert(1, raw_input("CLASS:"))
		else:
			continue

except KeyboardInterrupt:
	# write back to a new file
	with open(sys.argv[2], 'wb') as output_csvfile:
		writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

		# write each row in the csv file
		for i in data:
			writer.writerow(i)

	print '\n'
	sys.exit()
	

# write back to a new file
with open(sys.argv[2], 'wb') as output_csvfile:
	writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

	# write each row in the csv file
	for i in data:
		writer.writerow(i)
