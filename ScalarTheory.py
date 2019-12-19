from HyperCubic import *
import numpy
import copy

#make a general Theory class where field is replaced with multiple types of fields living on diff. elements of the lattice
class ScalarTheory:
	def __init__(self, dims, Action, obs = [], start = "cold"):
		self.field = HyperCubic(dims);
		self.action = Action;
		self.observables = obs;
		if start == "hot":
			for i in range(len(self.field.sites)):
				self.field.sites[i].value = numpy.random.normal(0.,1.);
		if start == "cold":
			for i in range(len(self.field.sites)):
				self.field.sites[i].value = 0.;

	def hotStart():
		for i in range(len(self.field.sites)):
			self.field.sites[i].value = numpy.random.normal(0.,1.);

	def coldStart():
		for i in range(len(self.field.sites)):
			self.field.sites[i].value = 0.;
	
	def __str__(self):
		output = "beta = " + str(self.action.beta) + "\n"; 
		output += str(self.field);
		output += "total action = " + str(self.action.total(self.field)) + "\n";
		for obs in self.observables:
			output += obs.name + ": " + str(obs.measure(self.field)) + "\n";
		return output;

class ScalarMove:
	def __init__(self, name = "", eps = 1.0):
		self.name = name;
		self.accepts = 0;
		self.rejects = 0;
		self.eps = eps;
	def move(self, phi_x):
		phi_x.value = numpy.random.normal(phi_x.value, self.eps);

	def __str__(self):
		output = "move " + str(self.name) + ": rejects = " + str(self.rejects) + ", accepts = " + str(self.accepts);
		output += "\neps: " + str(self.eps) + "\n";
		return output;