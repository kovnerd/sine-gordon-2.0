from HyperCubic import *
import math
import numpy
from ActionBase import *

class Action(ActionBase):
	def __init__(self, **kwargs):
		self.beta = kwargs["beta"];
		self.m = kwargs["bareMass"];
		self.a = kwargs["latticeSpacing"];
	
	#local action is correct - dont change it!
	def local(self, phi_x):
		sumOverNeighbors = 0.;
		for adj in phi_x.mu:
			sumOverNeighbors += adj.value;
		return self.beta*(0.5*((self.m*self.a)**2 + len(phi_x.mu))*phi_x.value**2 - phi_x.value*sumOverNeighbors);

	def total(self, phi):
		totAction = 0.;
		for coord in phi.coords:
			sumOverNeighbors = 0.;
			for adj in phi_x.mu:#sum over forward neighbors in total action
				sumOverNeighbors += adj.value;
			totAction += self.beta*(0.5*(2*len(phi.dims)+(self.m*self.a)**2)*phi_x.value**2 - phi_x.value*sumOverNeighbors);
		return totAction;

	def force(self, phi_x):
		sumOverNeighbors = 0.;
		for adj in phi_x.mu:
			sumOverNeighbors += adj.value;
		return self.beta*((len(phi_x.mu) + (self.m*self.a)**2)*phi_x.value - sumOverNeighbors);

	# "no ma" has a better picture: this will be the default from now on...
	def prop(self, phi, momCoord): 
		kOver2 = numpy.asarray([(numpy.pi*momCoord[i])/phi.dims[i] for i in range(len(momCoord))]);
		return 1. / (self.beta*(4.0*numpy.dot(numpy.sin(kOver2), numpy.sin(kOver2))/(self.a)**2 + (self.m)**2));#no ma
		#return 1./(self.beta*(4.0*numpy.dot(numpy.sin(kOver2), numpy.sin(kOver2)) + (self.m*self.a)**2));# with ma
		
	def weight(self, old, new, move=None):
		deltaS = self.local(new) - self.local(old);
		if(deltaS < 0):
			return 1.;
		else:
			return numpy.exp(-deltaS);