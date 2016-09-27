import sys
import csv

with open('data_test.py.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	data = list(reader)

data[0].insert(1, "PRESENT2012")
data[0].insert(1, "PRESENT2013")
data[0].insert(1, "PRESENT2014")
data[0].insert(1, "NUMOASIS")


for i in range(1, len(data)):

	twelve = 0
	thirteen = 0
	fourteen = 0

	for j in range(1, len(data[i]), 5):
		if "2012-09-23" in data[i][j] and data[i][j+2] == "FULL":
			twelve = 1
		if "2013-09-22" in data[i][j] and data[i][j+2] == "FULL":
			thirteen = 1
		if "2014-09-28" in data[i][j] and data[i][j+2] == "FULL":
			fourteen = 1

	if twelve == 1:
		data[i].insert(1, "1")
	else:
		data[i].insert(1, "0")

	if thirteen == 1:
		data[i].insert(1, "1")
	else:
		data[i].insert(1, "0")

	if fourteen == 1:
		data[i].insert(1, "1")
	else:
		data[i].insert(1, "0")

	temp = 0
	for j in range(5, len(data[i]), 5):
		if "Oasis" in data[i][j] and "2015-09-20" not in data[i][j-1]:
			temp += 1

	data[i].insert(1, str(temp))

with open('output.csv', 'wb') as output_csvfile:
	writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

	for i in data:
		writer.writerow(i)