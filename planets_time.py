#!/usr/bin/python

import numpy
import pylab
import sys
import matplotlib.pyplot as plt
import os
import urllib2
import datetime
import re

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
start_year = 1990
planets = [0.0 for x in range(start_year, datetime.datetime.now().year+1)]
years = [(float)(x) for x in range(start_year, datetime.datetime.now().year+1)]
kepler_start_year = 2009
kepler_planets = [0.0 for x in range(kepler_start_year, datetime.datetime.now().year+1)]
kepler_years = [(float)(x) for x in range(kepler_start_year, datetime.datetime.now().year+1)]
for i in range(0, len(data)):
    try:
        year = int(data[i].split('\t')[14])
    except ValueError,e:
        continue;
    if (year >= start_year):
        # cumulative
        for j in range(year, datetime.datetime.now().year+1):
            planets[j-start_year] += 1.0;
        if (re.match('^Kepler-',data[i].split('\t')[0])):
            for j in range(year, datetime.datetime.now().year+1):
                kepler_planets[j-kepler_start_year] += 1.0;

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.set_title("Discovered exoplanets")

# X axis
ax1.set_xlabel('Year')
ax1.set_xlim(start_year,datetime.datetime.now().year)
ax1.set_xticks([1990,2000,2010])

# Y axis
ax1.set_ylabel('Number')
ax1.set_yticks([200,400,600])


ax1.plot(years, planets, 'r', lw=1, label='total')
ax1.plot(kepler_years, kepler_planets, 'b', lw=1, label='Kepler')

ax1.annotate('Total', (years[15], planets[15]+10), xytext=(-80, 60), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle = "-", connectionstyle = "arc3,rad=-0.5", linewidth = 2))
ax1.annotate('Kepler', (kepler_years[3], kepler_planets[3]+10), xytext=(-30, 40), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle = "-", connectionstyle = "arc3,rad=-0.1", linewidth = 2))

import XKCDify
#XKCDify the axes -- this operates in-place
XKCDify.XKCDify(ax1, xaxis_arrow='+', yaxis_arrow='+', expand_axes=False)

# save file
basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
pylab.savefig(basename + '.pdf')
