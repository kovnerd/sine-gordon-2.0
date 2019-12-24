import Flow as FL
import Scheduler as SCHED
from ScalarTheory import *
from MiscAlgo import *
import Observables as OBS
import SineGordon as SG
import FreeField as FREE
import Metropolis as MET
import numpy
import Simulation as SIM
import matplotlib.pyplot as plt
from matplotlib import colors
import itertools as it


#CODE PART
#MAKE SURE ENSEMBLE IS SAVED CORRECTLY
#maybe replace linked-list nearest neighbor storage with something faster...?

#FLOW PART:
#MAKE FLOW SIM: rewrite flow sim
#MAKE KL DIV OBSERVABLE: TAKES IN ENTIRE ENSEMBLE(S)
#WORK ON RG FLOW EQUATION: TRY 0th ORDER FIRST

#fft even size is still broken
#fft odd size works, nor sure why...


def main():
	Nsteps = 100;
	size = 32;
	dims = [size, size];
	temp = 1.;
	mass = 1.;
	a = 0.2;
	algName = "FFT even size testing";
	obs = [OBS.Propagator2D(latticeSpacing = a)];
	obs.append(OBS.MomentumPropagator2D(latticeSpacing = a));
	print(algName);
	
	#sg = ScalarTheory([size, size], SG.Action(1./temp), obs, "cold");
	#flow = FL.Flow(FL.FreeToSG0(beta = 1./temp), intType = "euler", isEven = sg.field.isEven, indices = sg.field.coords, nSteps = Nsteps, stepSize = 1./Nsteps);	

	#'''
	#WHY IS THIS SO NOISY FOR EVEN SIZE...?
	free = ScalarTheory(dims, FREE.Action(beta = 1./temp, bareMass = mass, latticeSpacing = a), obs, "cold");
	fft = FourierAcceleration2D();
	sim = SIM.InstantSimulation(observables = obs, ensembleSize = 3000, mode = "measurements");
	results = sim.run(free, fft);
	#'''
	
	'''
	free = ScalarTheory(dims, FREE.Action(beta = 1./temp, bareMass = mass, latticeSpacing = a), obs, "cold");
	met = MET.MetropolisSingleSite(SCHED.Explicit([ScalarMove(eps = 1.5)]), free.action.weight);
	sim = SIM.Simulation(observables = obs, ensembleSize = 2000, corSweeps = 500, thermTime = 4096, mode = "measurements");
	results = sim.run(free, met);
	#'''

	prop = numpy.average(results["prop 2D"], axis = 0);
	massMeasured = (1./a)*numpy.log(numpy.abs(prop[:-1]/prop[1:]));
	momProp = numpy.average(results["mom prop 2D"], axis = 0);

	#'''
	print(algName);
	print("position space propagator: " + str(prop));
	print("extracted mass: " + str(massMeasured));
	print("input mass: " + str(mass));
	print("input lattice spacing: " + str(a));
	#'''	
	timeSeps = a*(numpy.asarray(range(size)));
	
	
	#'''
	fig1 = plt.figure(1);
	plt.plot(timeSeps, prop);#change to prop/prop[0] afterwards
	plt.xlabel("t");
	plt.ylabel("<G(t)>");
	fig1.savefig("obsPROP_alg" + str(algName) + "_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) + "_ensSize_" + str(sim.ensembleSize) + ".jpg");
	#'''
	#'''
	fig2 = plt.figure(2);
	plt.plot(timeSeps[1:], massMeasured);
	plt.xlabel("t");
	plt.ylabel("<m>");
	fig2.savefig("obsEFFMASS_alg" + str(algName) + "_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) +  "_ensSize_" + str(sim.ensembleSize) + ".jpg");
	#'''

	#'''
	fig3 = plt.figure(3);
	pos = plt.imshow(momProp, cmap = "jet");
	fig3.colorbar(pos);
	plt.title("momentum propagator from ensemble")
	plt.xlabel("x");
	plt.ylabel("y");
	fig3.savefig("obsMOMPROP_alg" + str(algName) + "_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) +  "_ensSize_" + str(sim.ensembleSize) + ".jpg");
	#'''
	
	momPropExpected = numpy.zeros(free.field.dims);
	for i, j in it.product(range(dims[0]), range(dims[1])):
		if (i,j) <= (dims[0]//2, dims[1]//2):
			mom = (i,j);
		elif i <= dims[0]//2 and j > dims[1]//2:
			mom = (i, j-dims[1]);
		elif i > dims[0]//2 and j <= dims[1]//2:
			mom = (i-dims[0], j);
		else:
			mom = (i-dims[0], j-dims[1]);
		momPropExpected[(i,j)] = free.action.prop(free.field, mom);

	fig4 = plt.figure(4);
	pos2 = plt.imshow(momPropExpected, cmap = "jet");
	fig4.colorbar(pos2);
	plt.title("momentum propagator from analytic calculations")
	plt.xlabel("x");
	plt.ylabel("y");
	plt.show();


	fig5 = plt.figure(5);
	pos3 = plt.imshow(numpy.abs(momPropExpected - momProp), cmap = "jet");
	fig5.colorbar(pos3);
	plt.title("standard error in momentum propagator")
	plt.xlabel("x");
	plt.ylabel("y");
	plt.show();
	fig5.savefig("obsMOMPROP_STDERR_alg" + str(algName) + "_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) +  "_ensSize_" + str(sim.ensembleSize) + ".jpg");
	plt.close();
main()