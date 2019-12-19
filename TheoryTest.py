import SineGordon as SG
import FreeField as FREE
import MiscAlgo as MISC
import Scheduler as SCHED
import Observables as OBS
import Metropolis as MET
import Simulation as SIM
from ScalarTheory import *
import copy
import matplotlib.pyplot as plt
from matplotlib import colors


	# GOOD CODE PROGRESS:
	#	HyperCubic (links++)			(NO)

	#	I/O:							
		# Store Output					(NO)
		# Parse Input 					(NO)

def main():
	temp = 25.1327;
	size = 64;
	obs = [OBS.Roughness()];
	sg = ScalarTheory([size, size], SG.Action(1./temp), obs, "hot");
	mcmoves = SCHED.Explicit([ScalarMove(eps = 5.0)]);
	met = MET.MetropolisWithOverrelax(mcmoves, sg.action.weight, SG.OverrelaxMove());
	#met = MET.Metropolis(mcmoves, sg.action.weight);

	ensembleSize = 256;
	corSweeps = 256;
	thermTime = 2048;

	sim = SIM.Simulation(observables = sg.observables, thermTime = thermTime, corSweeps = corSweeps, ensembleSize = ensembleSize, mode = "measurements");
	measurements = sim.run(sg, met);
	
	'''
	size = 16;
	temp = 1.;
	mass = 1.;
	a = 0.2;
	trivial = ScalarTheory([size, size], FREE.Action(beta = 1./temp, mass = mass*a, space = "p"), None, "hot");
	sim = SIM.InstantSimulation(observables = obs, ensembleSize = 1, mode = "ensemble");
	rand = MISC.RandomGaussians(loc = 0., width = numpy.sqrt(1./2.*trivial.beta));
	results = sim.run(free, rand);
	'''
	#make flow object
	#run flow sim





main();