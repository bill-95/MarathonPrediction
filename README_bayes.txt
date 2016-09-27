Naive Bayes for the classification of whether or not a runner will participate in the 2016 Montreal Marathon

From the command line you can execute the file given:

python y1_naive_bayes.csv naive_bayes_data.csv naive_bayes_output.csv

You can use any name for the last argument and it will give you a column with all of the predictions in a csv file.


input file should be as follows:
ID | PRESENT2015 | PRESENT2014 | PRESENT2013 | PRESENT2012 | NUMOASIS
01 |     0       |     1       |     1       |     0       |     3    
.........
