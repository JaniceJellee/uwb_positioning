import csv
import math
import numpy as np
from transformations import euler_from_quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# import pandas as pd
# import statsmodels.formula.api as sm

import matplotlib.pyplot as plt
# import seaborn as sns

f = open('data.csv')
csv_f = csv.reader(f)

x_means = []
y_vars = []


#n = 0 
current_predicted_dists = []

for row in csv_f:
    if len(row) == 0 or row[0] == "" or row[0] == "\x1a":
#        print ("NEW LINE")

        # ANALYZE SEGMENT
        if len(current_predicted_dists) > 0:
            # calculate avg of measured dists and angles
            mean = sum(current_predicted_dists)/len(current_predicted_dists)
            x_means.append(mean)
            
            # calculate variance
            var = np.var(current_predicted_dists)
            y_vars.append(var)
       
            # reset
            current_predicted_dists = []
    
    else:
        current_predicted_dists.append(float(row[0]))
#       
f.close()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.set_xlabel('Distance (m)')
# ax.set_ylabel('Angle (rad)')
# ax.set_zlabel('Variance')
# #ax.scatter(x_actual_dists, y_angles, z_vars)
# #ax.plot_wireframe(x_actual_dists, y_angles, z_vars)
# #ax.plot_surface(x_actual_dists, y_angles, z_vars)

# # to see range
# print ("MIN DIST:", min(x_actual_dists))
# print ("MAX DIST:", max(x_actual_dists))
# print ("MIN ANG:", min(y_angles))
# print ("MAX ANG:", max(y_angles))

# gets x y z triplets
FILE_PATH = "/Users/Janice/Dropbox (MIT)/Documents/Summer UROP/uwb_variance/data/datapoints.csv"

f = open(FILE_PATH, "w", newline="")
writer = csv.writer(f, delimiter=',', quotechar='"')
writer.writerow(['mean', 'var'])
writer.writerow([])

for i in range(len(x_means)):
   writer.writerow([x_means[i],y_vars[i]])
f.close()

# organize into ranges
# FILE_PATH = "/Users/Janice/Dropbox (MIT)/Documents/Summer UROP/uwb_variance/data/rectangle.csv"

# f = open(FILE_PATH, "w", newline="")
# writer = csv.writer(f, delimiter=',', quotechar='"')
# writer.writerow(['actual dist', 'angle', 'var'])
# writer.writerow([])

# for i in range(len(x_actual_dists)):
#     dist = x_actual_dists[i]
#     ang = y_angles[i]
#     x = str(round((int((dist/.25))*.25), 2)) + "-" + str(round((int((dist/.25))*.25)+.25, 2))
#     y = str(round((int((ang/.2))*.2), 1)) + "-" + str(round((int((ang/.2))*.2)+.2, 1))
#     z = z_vars[i]
#     writer.writerow([x, y, z])
# f.close()


