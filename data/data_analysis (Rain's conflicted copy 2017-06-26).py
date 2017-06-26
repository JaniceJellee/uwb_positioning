import csv

f = open('combined_data.csv')
csv_f = csv.reader(f)

x_actual_distances = []
y_angles = []
z_variance = []

n = 0 

for row in csv_f:
	if len(row) == 0:
		print ("NEW LINE")
	elif row[0].isNumeric():
		print ("FLOATY")
	elif type(row[0]) == str:
		print ("HEADING")
	n+=1
	if n > 10:
		break

f.close()