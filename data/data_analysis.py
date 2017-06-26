import csv
import math
import numpy as np
# from transformations import euler_from_quaternion

f = open('data1.csv')
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
    if len(row) == 0:
        print ("NEW LINE")

        # ANALYZE SEGMENT
        if len(current_predicted_dists) > 0:
#            # calculate avg of measured dists and angles
#            avg_measured_dist = sum(current_measured_dists)/len(current_measured_dists)
#            # avg_measured_ang = sum(current_measured_angs)/len(current_measured_angs)
#            x_actual_dists.append(avg_measured_dist)
#            # y_angles.append(avg_measured_ang)
#            
#            # calculate variance
#            var = np.var(current_predicted_dists)
#            z_vars.append(var)
       
            # reset
            current_predicted_dists = []
            current_measured_dists = []
            current_measured_angs = []

    elif row[0] == "predicted distance":
        print ("HEADING")
    else:
#        print (row)
        # add predicted distance
        current_predicted_dists.append(row[Labels.pred_dist])

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
        print (euler_from_quaternion([row[Labels.tag_rotx],
                                      row[Labels.tag_roty],
                                      row[Labels.tag_rotz],
                                      row[Labels.tag_rotw]]))


#    n += 1
#    if n > 1000:
#        break

#a=-0.00173689491689424
#b=-0.00155748098412418
#c=-0.00221348830732012
#d=0.999994828945902
#print (euler_from_quaternion([a,b,c,d]))
#
#
#a=0.009377357
#b=-0.005189062
#c=0.999929659
#d=-0.005080968
#print (euler_from_quaternion([a,b,c,d]))
#
#a=-0.000339929	
#b=-0.01273209	
#c=0.813617824	
#d=0.58126054
#print (euler_from_quaternion([a,b,c,d]))

f.close()