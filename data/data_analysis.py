import csv
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
# import pandas as pd
# import statsmodels.formula.api as sm

import matplotlib.pyplot as plt
# import seaborn as sns

f = open('all_data.csv')
csv_f = csv.reader(f)

x_yards = [5, 10, 15, 20, 25, 30, 40, 45, 25, 50,
          60, 65, 55, 75, 70, 80, 85, 90, 95, 100]
x_dists = []
for dist in x_yards:
	x_dists.append(dist/1.0936)
y_vars = []

current_predicted_dists = []

for row in csv_f:
    if len(row) == 0 or row[0] == "" or row[0] == "\x1a":
        print ("NEW LINE")

        # ANALYZE SEGMENT
        if len(current_predicted_dists) > 0:
            
            # calculate variance
            var = np.var(current_predicted_dists)
            y_vars.append(var)
       
            # reset
            current_predicted_dists = []
    
    else:
        current_predicted_dists.append(float(row[0]))
#       
f.close()
print (x_dists)
print (y_vars)

plt.plot(x_dists, y_vars, 'ro')
plt.xlabel("Distance (m)")
plt.ylabel("Variance")

# gets x y pairs
FILE_PATH = "/Users/Janice/Dropbox (MIT)/Documents/Summer UROP/uwb_variance/data/datapoints.csv"

f = open(FILE_PATH, "w", newline="")
writer = csv.writer(f, delimiter=',', quotechar='"')
writer.writerow(['distance', 'variance'])
writer.writerow([])

for i in range(len(x_dists)):
   writer.writerow([x_dists[i], y_vars[i]])
f.close()