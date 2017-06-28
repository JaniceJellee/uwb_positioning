import csv
import math
import numpy as np
from transformations import euler_from_quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import statsmodels.formula.api as sm

import matplotlib.pyplot as plt
import seaborn as sns

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

f = open('combined_data.csv')
csv_f = csv.reader(f)

x_actual_dists = []
y_angles = []
z_vars = []

class Labels(object):
    pred_dist = 0
    tag_transx = 1
    tag_transy = 2
    tag_transz = 3
    tag_rotx = 4
    tag_roty = 5
    tag_rotz = 6
    tag_rotw = 7
    home_transx = 8
    home_transy = 9
    home_transz = 10
    home_rotx = 11
    home_roty = 12
    home_rotz = 13
    home_rotw = 14

n = 0 
current_predicted_dists = []
current_measured_dists = []
current_measured_angs = []

for row in csv_f:
    if len(row) == 0 or row[0] == "" or row[0] == "\x1a":
#        print ("NEW LINE")

        # ANALYZE SEGMENT
        if len(current_predicted_dists) > 0:
            # calculate avg of measured dists and angles
            avg_measured_dist = sum(current_measured_dists)/len(current_measured_dists)
            avg_measured_ang = sum(current_measured_angs)/len(current_measured_angs)
            x_actual_dists.append(avg_measured_dist)
            y_angles.append(avg_measured_ang)
            
            # calculate variance
            var = np.var(current_predicted_dists)
            z_vars.append(var)
       
            # reset
            current_predicted_dists = []
            current_measured_dists = []
            current_measured_angs = []

    elif row[0] == "predicted distance":
#        print ("HEADING")
        continue
    
    else:
#        print (row)
        # add predicted distance
#        print (row[Labels.pred_dist])
        current_predicted_dists.append(float(row[Labels.pred_dist]))
#        print (current_predicted_dists)
        # add measured distance
        x1, y1, z1 = float(row[Labels.tag_transx]), \
                     float(row[Labels.tag_transy]), \
                     float(row[Labels.tag_transz])
        x2, y2, z2 = float(row[Labels.home_transx]), \
                     float(row[Labels.home_transy]), \
                     float(row[Labels.home_transz])

        dist = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2) \
             + math.pow(z1-z2, 2))
#        print (dist)
        current_measured_dists.append(dist)
        
        angle_tag = euler_from_quaternion([row[Labels.tag_rotx],
                                      row[Labels.tag_roty],
                                      row[Labels.tag_rotz],
                                      row[Labels.tag_rotw]], axes="sxyz")
        angle_home = euler_from_quaternion([row[Labels.home_rotx],
                                      row[Labels.home_roty],
                                      row[Labels.home_rotz],
                                      row[Labels.home_rotw]], axes="sxyz")
        a1 = angle_tag[2]
        if a1 < 0:
            a1 += math.pi
        a2 = angle_home[2]
        angle = a1 - a2
        if angle > math.pi/2:
            angle = math.pi - angle
        current_measured_angs.append(angle)
#        print (angle, angle_tag[2], angle_home[2])

#    n += 1
#    if n > 1000:
#        break

f.close()
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Angle (rad)')
ax.set_zlabel('Variance')
#print (x_actual_dists)
#print (y_angles)
#print (z_vars)
#ax.scatter(x_actual_dists, y_angles, z_vars)
#ax.plot_wireframe(x_actual_dists, y_angles, z_vars)
#ax.plot_surface(x_actual_dists, y_angles, z_vars)

data = pd.DataFrame({"X": x_actual_dists, "Y": y_angles, "Z": z_vars})
result = sm.ols(formula="Z ~ np.power(X, .005) + np.power(Y, .5)", data=data).fit()

print (result.params)
print (result.summary())


# Doesn't work yet 
## create some random data; replace that by your actual dataset
#data = pd.DataFrame({"X": x_actual_dists, "Y": y_angles, "Z": z_vars})
#
## plot heatmap
#ax = sns.heatmap(data.T)
#
## turn the axis label
#for item in ax.get_yticklabels():
#    item.set_rotation(0)
#
#for item in ax.get_xticklabels():
#    item.set_rotation(90)
#
## save figure
#plt.savefig('seabornPandas.png', dpi=100)
#plt.show()