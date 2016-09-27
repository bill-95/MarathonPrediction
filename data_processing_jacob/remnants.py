# calculates the mean of each feature
def mean(data):

	means = []

	# insert placeholder values; goes two less that number of columns to account for the ID column and present column
	for i in range(0, (len(data[0]) - 2)):
			means.insert(i, 0.0)

	# sum the values
	for i in range(0, len(data)):
		for j in range(0, (len(data[0]) - 2)):
			means[j] += float(data[i][j + 2])

	# divide the values by the number of rows 
	for i in range(0, len(means)):
			means[i] = means[i] / (len(data))

	return means


# calculate the standard deviations for all of the features
def stdevs(data):
	temp = [[],[],[],[],[]]

	for i in range(len(data)):
		for j in range(len(temp)):
			temp[j].append(float(data[i][j+2]))

	stdevs = []

	for i in temp:
		stdevs.append(statistics.stdev(i))

	return stdevs