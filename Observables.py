import numpy
import scipy
import itertools as it
from joblib import Parallel, delayed

class Observable:
	def __init__(self, name = ""):
		self.name = name;
	def measure(self, phi):
		pass;

class Explicit(Observable):
	def __init__(self, name, fnc):
		super(Explicit, self).__init__(name);
		self.fnc = fnc;
	def measure(self, phi):
		return self.fnc(phi);
		

#make parallel:
class FieldAverage(Observable):
	def __init__(self):
		super(FieldAverage, self).__init__(name = "field average");

	def measure(self, phi):
		phiTot = 0.;
		for field in phi.sites:
			phiTot += field.value;
		return phiTot/(len(phi));

#make parallel:
class Roughness(Observable):
	def __init__(self):
		super(Roughness, self).__init__(name = "roughness");

	def measure(self, phi):
		phiTot = 0.;
		phiTot2 = 0.;
		for field in phi.sites:
			phiTot += field.value;
			phiTot2 += field.value*field.value;
		return phiTot2/(len(phi)) - ( phiTot/(len(phi)) * phiTot/(len(phi)) );

class AverageLocal(Explicit):
	def __init__(self, name, localAction):
		super(AverageLocal, self).__init__(name, fnc = localAction);

	def measure(self, phi):
		actionTot = 0.;
		for field in phi.sites:
			actionTot += self.fnc(field);
		return actionTot/len(phi);


class CorrelationFunction1D(Observable):
	def __init__(self, sep, name = "corr fnc 1D"):
		super(CorrelationFunction1D, self).__init__(name);
		self.sep = sep;

	def measure(self, phi):
		prod = 0.;
		for t in range(phi.dims[0]):
			prod += phi[[t+self.sep]].value*phi[[t]].value;
		prod /= len(phi);
		return prod;


#do in parallel: make threads in measure() that each call super(...).measure(phi), and accumulate a sep
class Propagator1D(CorrelationFunction1D):
	def __init__(self, name = "prop 1D"):
		super(Propagator1D, self).__init__(0, name);

	def measure(self, phi):
		corfnc = [0. for i in range(int(phi.dims[0]))];
		for t in range(len(corfnc)):
			self.sep = t;
			corfnc[t] = super(Propagator1D, self).measure(phi);# I think this is how it works
		return corfnc;


class CorrelationFunction2D(Observable):
	def __init__(self, sep, latticeSpacing, name = "corr fnc 2D"):
		super(CorrelationFunction2D, self).__init__(name);
		self.T = sep;
		self.a = latticeSpacing;

	#extra statistics: maybe they are screwed up...?
	def measure(self, phi):
		prod = 0.;
		for t, x1, x2 in it.product(range(phi.dims[0]), range(phi.dims[1]), range(phi.dims[1])):
			prod += phi[(t+self.T, x2)].value*phi[(t, x1)].value;
		#'''
		#rotate for extra stats
		for t1, t2, x in it.product(range(phi.dims[0]), range(phi.dims[0]), range(phi.dims[1])):
			prod += phi[(t2, x+self.T)].value*phi[(t1, x)].value;
		#'''
		
		prod *= self.a**2 / (2*len(phi));#put lattice units back in???
		return prod;


#possibly parallelize this?
class Propagator2D(CorrelationFunction2D):
	def __init__(self, latticeSpacing = 1., name = "prop 2D"):
		super(Propagator2D, self).__init__(sep = 0, latticeSpacing = latticeSpacing, name = name);
		self.a = latticeSpacing;

	def measure(self, phi):
		corfnc = [0. for i in range(phi.dims[0])];
		for t in range(len(corfnc)):
			self.T = t;
			corfnc[t] = super(Propagator2D, self).measure(phi);# I think this is how it works


		return numpy.asarray(corfnc);#put lattice units back in


#written so that propagators don't have to be rewritten
class EffectiveMass:
	def __init__(self, latticeSpacing = 1., name = "eff mass"):
		self.a = latticeSpacing;

	def measure(self, prop):
		return (1./self.a)*numpy.log(numpy.abs(prop[:-1]/prop[1:]));

#TODO:
#Bootstrap: X
#KLDivergence: X
'''
#log(P,Q): in physics context these are actions
class KLDivergence:
	def __init__(self, name = "KL div"):

	def measure(ensembleP, logP, logQ):
		
'''

#make this a matrix
class MomentumPropagator2D(Observable):
	def __init__(self, latticeSpacing = 1., name = "mom prop 2D"):
		super(MomentumPropagator2D, self).__init__(name);
		self.a = latticeSpacing;

	def measure(self, phi):
		momLat = numpy.fft.ifftn(phi.toNumpy())*len(phi);
		momProp = momLat * numpy.conj(momLat);
		momProp = numpy.real(momProp);
		return momProp * self.a**2/len(phi);#put lattice units back in