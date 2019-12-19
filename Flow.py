import Scheduler as SCHED
import Integrator as INT
import numpy

#make this work for more than just Euler: change how the integrate method of generalized

class Flow(INT.Integrator):
	def __init__(self, action, **kwargs):
		super(Flow, self).__init__(action.force, **kwargs);
		self.action = action;
		self.lnDetJ = 0.;
		self.oldStep = self.integrator.step;
		self.integrator.step = self.step;

	#need to call old version of step as well!
	#need to somehow mix self.integrator.step with self.step
	def step(self, lat):
		for index in self.integrator.loop():
			self.lnDetJ += self.integrator.stepSize*self.action.forceDeriv(lat[index]);
		self.oldStep(lat);


#Various flow actions:

class FreeToSG0:
	def __init__(self, **kwargs):
		self.beta = kwargs["beta"];

	def total(self, lat):
		totalA = 0.;
		for phi_x in phi_x.sites:
			totalA += self.beta*numpy.cos(phi.value) - 1/(24.)*phi.value**4;
		return totalA;

	def local(self, phi):
		return self.beta*numpy.cos(phi.value) - 1/(24.)*phi.value**4;

	def force(self, phi):
		return self.beta*numpy.sin(phi.value) - 1/(12.)*phi.value**3;

	def forceDeriv(self, phi):
		return self.beta*numpy.cos(phi.value) - 1/4.*phi.value**2;

#make sure to implement the total method correctly: plot "loss function" like Chris does

#Assumes gaussian is generated at correct width: sigma^2 = 0.5*T
class GaussToSG0:
	def __init__(self, **kwargs):
		self.beta = kwargs["beta"];

	def total(self, lat):
		pass;

	def local(self, phi_x):
		sumOverNeighbors = 0.;
		for adj in phi_x.mu:
			sumOverNeighbors += adj.value;

		return self.beta*(-(1./6.)*phi_x.value**3*sumOverNeighbors + numpy.cos(phi_x.value));

	#Note, this is G = -dS/d(phi_x)
	def force(self, phi_x): 
		sumOverNeighbors = 0.;
		sumOverNeighbors3 = 0.;
		for adj in phi_x.mu:
			sumOverNeighbors += adj.value;
			sumOverNeighbors3 += adj.value**3;

		return self.beta*(0.5*(phi_x.value**2)*sumOverNeighbors + (1./6.)*sumOverNeighbors3 + numpy.sin(phi_x.value));

	def forceDeriv(self, phi_x):
		sumOverNeighbors = 0.;
		for adj in phi.mu:
			sumOverNeighbors += adj.value;
		return self.beta*(phi_x.value*sumOverNeighbors - numpy.cos(phi_x.value));