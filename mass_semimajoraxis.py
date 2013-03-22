#!/usr/bin/python

import numpy
import pylab
import sys
import matplotlib.pyplot as plt
import os
import urllib2

# check if we already have a caching directory
if not os.path.isdir('cache'):
    os.makedirs('cache')

# check if file exists and if not download it!
if not os.path.exists('cache/open_exoplanet_catalogue.txt'):
    fhandle = urllib2.urlopen('https://raw.github.com/hannorein/oec_tables/master/tab_separated/open_exoplanet_catalogue.txt')
    open('cache/open_exoplanet_catalogue.txt', 'wb').write(fhandle.read())

# read in file
with open("cache/open_exoplanet_catalogue.txt") as f:
    data = f.read()

# make array
data = data.split('\n')

# remove comment lines
data = filter(lambda x:not x.strip().startswith('#') , data)

# remove columns with not enough rows
data = filter(lambda x:x.count('\t') == 23, data)

# read from data into arrays (only valid data!)
mass_array = []
semi_major_axis_array = []
colors = []

for i in range(0, len(data)):
    try:
        mass = float(data[i].split('\t')[2])
        semi_major_axis = float(data[i].split('\t')[5])
    except ValueError,e:
        continue;
    mass_array.append(mass)
    semi_major_axis_array.append(semi_major_axis)
    colors.append(1)


fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.set_title("Exoplanet diversity")    

# X axis
ax1.set_xlabel('Semi-major axis')
ax1.set_xscale('log')
ax1.set_xlim(0.005,1000)

# Y axis
ax1.set_ylabel('Mass')
ax1.set_yscale('log')
ax1.set_ylim(0.001,50)

x1 = numpy.linspace(1, 10, 100)
x2 = numpy.linspace(1, 10, 100)

ax1.plot(semi_major_axis_array, mass_array, 'o', markerfacecolor='red', markeredgecolor='darkred', label='the data')

ax1.set_xticks([1e-2, 1e-1, 1, 10, 100])
ax1.set_yticks([1e-2,1e-1,1,10])

mass_earth = 1.0/320.0
distance_earth = 1.0
mass_jupiter = 1.0
distance_jupiter = 5.2

ax1.annotate('Earth', (distance_earth, mass_earth), xytext=(20, 20), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle = "->", connectionstyle = "angle,angleA=5,angleB=74,rad=10", linewidth = 2))
ax1.annotate('Jupiter', (distance_jupiter, mass_jupiter), xytext=(20, -20), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle = "->", connectionstyle = "arc,angleA=0,armA=20,angleB=-90,armB=15,rad=7", relpos=(0.5,0.5), linewidth = 2))

import XKCDify
#XKCDify the axes -- this operates in-place
XKCDify.XKCDify(ax1, xaxis_arrow='+', yaxis_arrow='+', expand_axes=False)

# save file
basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
pylab.savefig(basename + '.pdf')
