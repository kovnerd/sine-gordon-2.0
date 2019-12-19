import Flow as FL
import Scheduler as SCHED
from ScalarTheory import *
from MiscAlgo import *
import Observables as OBS
import SineGordon as SG
import FreeField as FREE
import Metropolis as MET
import numpy
import scipy
import Simulation as SIM
import matplotlib.pyplot as plt




#TEST SAVING ENSEMBLE
#MAKE FLOW SIM
#MAKE KL DIV OBSERVABLE: TAKES IN ENTIRE ENSEMBLE(S)
#WORK ON RG FLOW EQUATION: TRY 0th ORDER FIRST

def main():
	Nsteps = 100;
	size = 15;
	temp = 1.;
	mass = 1.;
	a = 0.2;
	algName = "FFT with norm extra stats";
	obs = [OBS.Propagator2D()];
	print(algName);
	
	#sg = ScalarTheory([size, size], SG.Action(1./temp), obs, "cold");
	#flow = FL.Flow(FL.FreeToSG0(beta = 1./temp), intType = "euler", isEven = sg.field.isEven, indices = sg.field.coords, nSteps = Nsteps, stepSize = 1./Nsteps);
	

	#'''
	#WHY IS THIS SO NOISY...?
	free = ScalarTheory([size, size], FREE.Action(beta = 1./temp, bareMass = mass, latticeSpacing = a), obs, "cold");
	fft = FourierAcceleration2D();
	sim = SIM.InstantSimulation(observables = obs, ensembleSize = 3000, mode = "measurements");
	results = sim.run(free, fft);
	#'''
	
	'''
	free = ScalarTheory([size, size], FREE.Action(beta = 1./temp, bareMass = mass, latticeSpacing = a), obs, "hot");
	met = MET.MetropolisSingleSite(SCHED.Explicit([ScalarMove(eps = 1.5)]), free.action.weight);
	sim = SIM.Simulation(observables = obs, ensembleSize = 2000, corSweeps = 500, thermTime = 4096, mode = "measurements");
	results = sim.run(free, met);
	#'''

	prop = numpy.average(results["prop 2D"], axis = 0);
	massMeasured = (1./a)*numpy.log(numpy.abs(prop[:-1]/prop[1:]));



	print(algName);
	print("position space propagator: " + str(prop));
	print("extracted mass: " + str(massMeasured));
	print("lattice mass: " + str(mass));
			
	timeSeps = a*(numpy.asarray(range(size)));
	
	

	fig1 = plt.figure(1);
	plt.plot(timeSeps, prop/prop[0]);
	plt.xlabel("t");
	plt.ylabel("<G(t)/G(0)>");
	fig1.savefig("obsPROP_alg" + str(algName) + "_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) + "_ensSize_" + str(sim.ensembleSize) + ".jpg");
			
	fig2 = plt.figure(2);
	plt.plot(timeSeps[1:], massMeasured);
	plt.xlabel("t");
	plt.ylabel("<m>");
	fig2.savefig("obsEFFMASS_alg" + str(algName) + "_dims" + str(free.field.dims) + "_mass" + str(mass) + "_a" + str(a) + "_temp"+ str(temp) +  "_ensSize_" + str(sim.ensembleSize) + ".jpg");

	plt.show();


	#test zeroth order flow

main()