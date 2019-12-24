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
		quad = 0.5*(self.m**2 + len(phi_x.mu)/self.a**2);
		return self.beta*self.a**(0.5*len(phi_x.mu))*(quad*phi_x.value**2 - sumOverNeighbors/self.a**2 * phi_x.value);

	def total(self, phi):
		totAction = 0.;
		for coord in phi.coords:
			sumOverNeighbors = 0.;
			for adj in phi_x.mu:#sum over forward neighbors in total action
				sumOverNeighbors += adj.value;
			totAction += self.beta*self.a**(len(phi.dims))*(0.5*(2*len(phi.dims)/self.a**2+(self.m)**2)*phi_x.value**2 - phi_x.value*sumOverNeighbors/self.a**2);
		return totAction;

	def force(self, phi_x):
		sumOverNeighbors = 0.;
		for adj in phi_x.mu:
			sumOverNeighbors += adj.value;
		return self.beta*self.a**(0.5*len(phi_x.mu))*((len(phi_x.mu)/self.a**2 + (self.m)**2)*phi_x.value - sumOverNeighbors/self.a**2);

	def prop(self, phi, momCoord): 
		k = numpy.asarray([(2*numpy.pi*momCoord[i])/phi.dims[i] for i in range(len(momCoord))]);
		#return len(phi) / (self.beta*(4.0*numpy.dot(numpy.sin(k/2), numpy.sin(k/2))/(self.a)**(2-len(phi.dims)) + (self.m)**2 * (self.a)**len(phi.dims)));
		#return 1./ (self.beta*(4.0*numpy.dot(numpy.sin(k/2), numpy.sin(k/2))/(self.a)**(2-len(phi.dims)) + (self.m)**2 * (self.a)**len(phi.dims)));
		return 1./ (self.beta*(4.0*numpy.dot(numpy.sin(k/2), numpy.sin(k/2))/(self.a)**(2) + (self.m)**2));

	def weight(self, old, new, move=None):
		deltaS = self.local(new) - self.local(old);
		if(deltaS < 0):
			return 1.;
		else:
			return numpy.exp(-deltaS);