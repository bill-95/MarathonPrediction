import sys
import csv

# open the data file
with open(sys.argv[1], 'rb') as data_csvfile:
	reader = csv.reader(data_csvfile)
	data = list(reader)

# open the types file
with open(sys.argv[2], 'rb') as types_csvfile:
	reader = csv.reader(types_csvfile)
	types = list(reader)

remaining = []

full = types[0][1:]
half = types[1][1:]
ten = types[2][1:]
five = types[3][1:]
other = types[4][1:]

data[0].insert(1, "OTHER")
data[0].insert(1, "FIVE")
data[0].insert(1, "TEN")
data[0].insert(1, "HALF")
data[0].insert(1, "FULL")

for i in range(1,len(data)):

	full_count = 0
	half_count = 0
	ten_count = 0
	five_count = 0
	other_count = 0

	for j in range(3, len(data[i]), 5):
		if any(s == data[i][j] for s in full):
			data[i][j] = "FULL"
			full_count+=1
		elif any(s == data[i][j] for s in half):
			data[i][j] = "HALF"
			half_count+=1
		elif any(s == data[i][j] for s in ten):
			data[i][j] = "TEN"
			ten_count+=1
		elif any(s == data[i][j] for s in five):
			data[i][j] = "FIVE"
			five_count+=1
		elif any(s == data[i][j] for s in other):
			data[i][j] = "OTHER"
			other_count+=1
		else:
			remaining.insert(0, [data[i][j]])


	data[i].insert(1, str(other_count))
	data[i].insert(1, str(five_count))
	data[i].insert(1, str(ten_count))
	data[i].insert(1, str(half_count))
	data[i].insert(1, str(full_count))




# write back to a new file
with open(sys.argv[3], 'wb') as output_csvfile:
	writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

	# write each row in the csv file
	for i in data:
		writer.writerow(i)

with open('remaining.csv', 'wb') as output_csvfile:
	writer = csv.writer(output_csvfile, quoting = csv.QUOTE_ALL)

	# write each row in the csv file
	for i in remaining:
		writer.writerow(i)
