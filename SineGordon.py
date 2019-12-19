import numpy
import math
#import tensorflow as tf
from ActionBase import *
from ScalarTheory import ScalarMove
from Observables import FieldAverage

class Action(ActionBase):
	def __init__(self, beta):
		self.beta = beta;

	def local(self, phi_x):#NOT RIGHT!?!?
		sumOverNeighbors = 0.;
		for adj in phi_x.mu:
			sumOverNeighbors += adj.value;
		return self.beta*0.5*(len(phi_x.mu)*phi_x.value**2 - 2*phi_x.value*sumOverNeighbors - 2*numpy.cos(phi_x.value) );

	def total(self, phi):#rewrite in terms of looping over phi.sites
		totAction = 0.;
		for phi_x in phi.sites:
			sumOverNeighbors = 0.;
			for adj in phi_x.mu[:len(phi_x.mu)]:#sum over forward neighbors in total action SUSPICIOUS
				sumOverNeighbors += adj.value;
			totAction += self.beta*( len(phi.dims)*phi_x.value*phi_x.value - phi_x.value*sumOverNeighbors - numpy.cos(phi_x.value));
		return totAction; 

	def force(self, phi_x):
		sumOverNeighbors = 0.;
		for adj in self.phi_x.mu:
			sumOverNeighbors += adj.value;
		return self.beta*(2*(len(phi_x.mu)//2)*phi_x.value - sumOverNeighbors + numpy.sin(phi_x.value));

	def weight(self, old, new, move=None):
		deltaS = self.local(new) - self.local(old);
		if(deltaS < 0):
			return 1.;
		else:
			return numpy.exp(-deltaS);

#'''
class OverrelaxMove(ScalarMove):
	def __init__(self):
		super(OverrelaxMove, self).__init__("overrelax");
		self.av = FieldAverage();
	def move(self, phi):#change
		phiAv = self.av.measure(phi);
		for phi_x in phi.sites:
			phi_x.value -= 2*numpy.pi*round(phiAv/(2*numpy.pi));
#'''