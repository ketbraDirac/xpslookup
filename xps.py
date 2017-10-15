# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:06:43 2017

@author: kgord
"""

import numpy as np

E_Center = 10
E_Width = 2

with open('xps_data.csv') as xps_table:
    header = xps_table.readline()
    header = header.strip().split(',')
    orbitals = header[3:]
    elements = []
    for line in xps_table:
        line = line.strip().split(',')
        elements.append(line[0:3])
energies = np.genfromtxt('xps_data.csv', delimiter=',', skip_header=1, usecols=range(3,27))
energies[np.isnan(energies)] = -np.inf
condition = np.abs(energies - E_Center) < E_Width
for match in np.argwhere(condition):
    elem = match[0]
    orb = match[1]
    print(elements[int(elem)][2], "\t" , orbitals[int(orb)], "\t", energies[int(elem), int(orb)])
