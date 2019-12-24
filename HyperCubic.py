#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import types
import numpy
import math
from Node import *

#ADD LINK AND PLAQUETTE FUNCTIONALITY LATER

class HyperCubic:
    def __init__(self, dims):
        self.dims = dims;
        numSites = 1;
        for d in dims:
            numSites *= d;
        self.sites = numpy.asarray([Node() for i in range(numSites)]);
        self.coords = [self.IndexToCoord(i) for i in range(numSites)];
        self.__buildNeighbors(); 

    def toNumpy(self):
        selfNumpy = numpy.zeros(len(self.sites));
        for i in range(len(self.sites)):
            selfNumpy[i]= self.sites[i].value;
        selfNumpy = numpy.reshape(selfNumpy, self.dims);
        return selfNumpy;

    def fromNumpy(self, selfNumpy):#hopefully this works
        for coord in self.coords:
            self.sites[self.CoordToIndex(coord)].value = selfNumpy[tuple(coord)];    

    #used to init
    def __buildNeighbors(self):
        numSites = len(self.sites);
        dims = self.dims;
        #neighbor by reference:
        for index in range(numSites): #PERIODIC BOUNDARY CONDITIONS
            for i in range(len(dims)):#forward neighbor indices
                self.sites[index].mu.append(self.__getitem__([(self.coords[index][j]+1)%dims[j] if i == j else self.coords[index][j] for j in range(len(dims))]));
            for i in range(len(dims)):#backward neighbor indices
                self.sites[index].mu.append(self.__getitem__([(self.coords[index][j]-1)%dims[j] if i == j else self.coords[index][j] for j in range(len(dims))]));

    def copy(self, lat):#expensive but necessary...
        for site in self.sites:
            site.copy(lat.site);
        self.dims = lat.dims;
        self.coords = lat.coords;

    def __getitem__(self, coord):#retrieves the site information
        return self.sites[self.CoordToIndex(coord)];

    def __setitem__(self, coord, item):#item has to be the whole site... nuts
        self.sites[self.CoordToIndex(coord)].value = item;

    def __str__(self):
        strlat =  "dims =" + str(self.dims) + "\n"
        for index in range(len(self.sites)):
            strlat += "site " + str(index) +", " + str(self.IndexToCoord(index)) + ": " + str(self.sites[index]) + "\n";
        return strlat;

    def __len__(self):#returns number of sites
        return len(self.sites);
    
    #convert len(dims) dimensional vector to 1D index  
    def CoordToIndex(self, coord): #do PBC
        i = 0;
        c = 1;
        #convert len(self.dims)-D coordinate to a 1D index
        for d in self.dims:
            c *= d;
        for j in range(len(self.dims)):
            c = c // self.dims[j];
            i += ((coord[j]+self.dims[j])%self.dims[j])*c;#PBC here
        return i;

    def IndexToCoord(self, index):
        c = 1;
        coord = [];
        for d in range(len(self.dims)):
            c *= self.dims[d];
        for d in range(len(self.dims)):
            c = c // self.dims[d];
            j = index//c;
            index -= j*c;
            coord.append(j);
        return coord;

    def isEven(self, coord):
        coordSum = numpy.sum(coord);
        if coordSum%2 == 0:
            return True;
        else:
            return False;
