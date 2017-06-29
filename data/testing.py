# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 00:25:14 2017

@author: Janice
"""
FILE_PATH = "/Users/Janice/Dropbox (MIT)/Documents/Summer UROP/uwb_variance/data/datapoints.csv"

f = open(FILE_PATH, "w", newline="")
writer = csv.writer(f, delimiter=',', quotechar='"')
writer.writerow(['actual dist', 'angle', 'var'])
writer.writerow([])

for i in range(len(x_actual_dists)):
    writer.writerow([1,2,3])
f.close()