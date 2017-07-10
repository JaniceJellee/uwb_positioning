# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 00:25:14 2017

@author: Janice
"""
#FILE_PATH = "/Users/Janice/Dropbox (MIT)/Documents/Summer UROP/uwb_variance/data/datapoints.csv"
#
#f = open(FILE_PATH, "w", newline="")
#writer = csv.writer(f, delimiter=',', quotechar='"')
#writer.writerow(['actual dist', 'angle', 'var'])
#writer.writerow([])
#
#for i in range(len(x_actual_dists)):
#    writer.writerow([1,2,3])
#f.close()

angle_labels = []
n = 0
for i in range(8):
    angle_labels.append(str(round(n, 1)) + "-" + str(round(n+0.2, 1)))
    n += 0.2
    
dist_labels = []
n = 0.25
for i in range(19):
    dist_labels.append(str(round(n, 2)) + "-" + str(round(n+0.25, 2)))
    n += 0.25
    
print (dist_labels)

n = .4
print (str(round((int((n/.2))*.2), 1)) + "-" + str(round((int((n/.2))*.2)+.2, 1)))
n = 4.6
y = str(round((int((n/.25))*.25), 2)) + "-" + str(round((int((n/.25))*.25)+.25, 2))
print (y)

    