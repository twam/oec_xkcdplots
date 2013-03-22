#!/usr/bin/python

import numpy
import pylab
import sys
import matplotlib.pyplot as plt
import os
import urllib2
import datetime

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

for i in range(0, len(data)):
    try:
        year = int(data[i].split('\t')[14])
    except ValueError,e:
        continue;
    if (year >= start_year):
        # cumulative
        for i in range(year, datetime.datetime.now().year+1):
            planets[i-start_year] += 1.0;

fig = plt.figure()
ax1 = fig.add_subplot(111)


ax1.set_title("Discovered exoplanets")

# X axis
ax1.set_xlabel('Year')
#ax1.set_xscale('log')
ax1.set_xlim(start_year,datetime.datetime.now().year)
ax1.set_xticks([1990,2000,2010])

# Y axis
ax1.set_ylabel('Number')
#ax1.set_yscale('log')
#ax1.set_ylim(0.001,50)
ax1.set_yticks([200,400,600])

ax1.plot(years, planets, 'r', lw=1)

import XKCDify
#XKCDify the axes -- this operates in-place
XKCDify.XKCDify(ax1, xaxis_arrow='+', yaxis_arrow='+', expand_axes=False)

# save file
basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
pylab.savefig(basename + '.pdf')
