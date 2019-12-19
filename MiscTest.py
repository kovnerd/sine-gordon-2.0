import Flow as FL
import Scheduler as SCHED
from ScalarTheory import *
from MiscAlgo import *
import Observables as OBS
import SineGordon as SG
import FreeField as FREE
import Metropolis as MET
import numpy
import itertools as it
import Simulation as SIM
import matplotlib.pyplot as plt

def main():
	#size = 4;
	#temp = 1.;
	#mass = 1.;
	#a = 0.2;
	#obs = [OBS.Propagator2D()];
	#free = ScalarTheory([size, size], FREE.Action(beta = 1./temp, mass = mass*a, space = "p"), obs, "hot");
	#sg = ScalarTheory([size, size], SG.Action(1./temp), obs, "hot");
	#flow = FL.Flow(FL.FreeToSG0(beta = 1./temp), intType = "euler", isEven = sg.field.isEven, indices = sg.field.coords, nSteps = Nsteps, stepSize = 1./Nsteps);
	
	#WORKS FOR ODD'S, NOT FOR EVENS???
	size = 7;
	dims = [size,size];
	a = numpy.random.normal(loc = 0, scale = 1., size = dims);
	#a = numpy.reshape(range(dims[0]*dims[1]), dims);
	b = numpy.zeros(dims, dtype = complex);
	print("a = \n" + str(a));
	print("afft = \n" + str(numpy.fft.fftn(a)))

	#THIS IS CORRECT:
	#
	if (dims[1]%2 == 0):#even N
		dims1End = dims[1]//2+1;#was +2 before, but +1 is working now...?
	else:#odd N
		dims1End = dims[1]//2+1;
	#

	#THIS IS CORRECT
	#'''
	for i, j in it.product(range(0, dims[0]), range(0, dims1End)):
		if i == 0 and j == 0:#origin
			b[(i,j)] = numpy.complex(a[(i,j)], 0);
		else:
			b[(i, j)] = numpy.complex(a[(i, j)], a[(i, j)]);
			if i == 0 and j != 0: # horizontal leg
				if j == dims[1] - j:
					b[(i, j)] = numpy.complex(a[(i,j)], 0);#make b[i,j] real
				else:
					b[(i, dims[1] - j)] = numpy.conjugate(b[(i, j)]); 
			elif i !=0 and j == 0: # vertical leg
				if i == dims[0] - i:
					b[(i, j)] = numpy.complex(a[(i,j)], 0);#make b[i,j] real
				else:
					b[(dims[0] - i, j)] = numpy.conjugate(b[(i, j)]); 
			else: #body
				if i == dims[0] - i and j == dims[1] - j:
					b[(i, j)] = numpy.complex(a[(i,j)], 0);#make b[i,j] real
				else:
					b[(dims[0] - i, dims[1] - j)] = numpy.conjugate(b[(i, j)]); 
	#'''

	print("b = \n" + str(b));
	bifft = numpy.fft.ifftn(b);
	print("bifft = \n" + str(bifft));
	print("imag part of bifft (should be 0's) = \n" + str(numpy.imag(bifft)));


	#fft = FourierAcceleration2D();
	#sim = SIM.InstantSimulation(observables = obs, ensembleSize = 1, mode = "measurements");
	#results = sim.run(free, fft);
	
	#Met works, but its unclear how to check if the mass is right
	#-> write momentum propagator code
	'''
	met = MET.MetropolisSingleSite(SCHED.Explicit([ScalarMove(eps = 1.0)]), free.action.weight);
	sim = SIM.Simulation(observables = obs, ensembleSize = 1000, corSweeps = 50, thermTime = 2048, mode = "measurements");
	results = sim.run(free, met);
	'''
	#prop = numpy.average(results["prop 2D"], axis=0);
	#prop = numpy.average(results["prop 1D"], axis=0);
	#massMeasured = 1/a*numpy.log(numpy.abs(prop[:-1]/prop[1:]));
	
	'''print("position space propagator: " + str(prop));
				print("extracted mass: " + str(massMeasured));
				print("input mass: " + str(mass));
			
				timeSeps = a*(numpy.asarray(range(size))+1);
			
			
				fig1 = plt.figure(1);
				plt.plot(timeSeps, prop);
				plt.xlabel("t");
				plt.ylabel("<G(t)>");
				fig1.savefig("obsPROP_algFFT_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) + ".jpg");
			
				fig2 = plt.figure(2);
				plt.plot(timeSeps[1:], massMeasured);
				plt.xlabel("t");
				plt.ylabel("<m>");
				fig2.savefig("obsEFFMASS_algFFT_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) + ".jpg");
				
				plt.show();'''

main();