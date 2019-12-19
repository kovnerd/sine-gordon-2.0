import copy
import progressbar as pg


#Maybe make other types simulations own Simulation instead of inheriting it

class Simulation:
	#make observables part of simInfo
	def __init__(self,  enableBars = False, **kwargs):
		self.thermTime = kwargs["thermTime"];
		self.ensembleSize = kwargs["ensembleSize"];
		self.corSweeps = kwargs["corSweeps"];
		self.mode = kwargs["mode"];#make mode part of simInfo?
		self.ensemble = [None for i in range(self.ensembleSize)];
		self.measurements = {};
		self.observables = {};
		self.enableBars = enableBars;
		if enableBars:
			thermWidgets = ['Thermalizing...', pg.Bar(marker = '=', left = '[', right = ']'), pg.Percentage()];
			self.thermBar = pg.ProgressBar(widgets = thermWidgets, max_value = self.thermTime);
			ensembleWidgets = ['Generating Data...', pg.Bar(marker = '=', left = '[', right = ']'), pg.Percentage()];
			self.ensembleBar = pg.ProgressBar(widgets = ensembleWidgets, max_value = self.ensembleSize);
		for obs in kwargs["observables"]:
			self.measurements[obs.name] = [None for n in range(kwargs["ensembleSize"])];
			self.observables[obs.name] = obs;

	#add progress bar and checkpointing?
	def thermalize(self, theory, algo):
		#self.thermBar.start();
		print("Thermalizing...");
		for i in range(self.thermTime):
			algo.update(theory);
			'''#
			if(i % 10 == 0):
				for name in self.observables:
					print(name + ":" +str(self.observables[name].measure(theory.field)));
				print("\n");
			'''
			#self.thermBar.update(i);
		print("Finished!");

	#MAKE SURE ENSEMBLE MODE IS WORKING CORRECTLY
	def produceEnsemble(self, theory, algo):
		#self.ensembleBar.start();
		print("Producing Ensemble...");
		if self.mode == "ensemble":
			for n in range(self.ensembleSize):
				for nc in range(self.corSweeps):
					algo.update(theory);
				self.ensemble[n] = copy.copy(theory.field);#Implement own copy function?
		#		self.ensembleBar.update(n);
		elif self.mode == "measurements":
			for n in range(self.ensembleSize):
				for nc in range(self.corSweeps):
					algo.update(theory);
				for name in self.observables:
					self.measurements[name][n] = self.observables[name].measure(theory.field);
				if(n % 10 == 0):
					for name in self.observables:
						print(name + " #" + str(n) + " :" + str(self.measurements[name][n]));
					print("\n");
					# print(name + ": " + str(self.measurements[name][n]));
				# print("\n");
		#		self.ensembleBar.update(n);
		else: #do both: not recommended
			for n in range(self.ensembleSize):
				for nc in range(self.corSweeps):
					algo.update(theory);
				self.ensemble[n] = copy.copy(theory.field);
				for name in self.observables:
					self.measurements[name][n] = self.observables.measure(theory.field);
				if(n % 10 == 0):
					for name in self.observables:
						print(name + " #" + str(n) + " :" + str(self.measurements[name][n]));
					print("\n");
		#		self.ensembleBar.update(n);
		print("Finished!");

	def run(self, theory, algo):
		self.thermalize(theory, algo);
		self.produceEnsemble(theory, algo);
		if self.mode == "measurements":
			return self.measurements;
		elif self.mode == "ensemble":
			return self.ensemble;
		else:
			return {"ensemble":self.ensemble, "measurements":self.measurements};


#Make Simulation a member variable instead?
class TemperatureSimulation(Simulation):
	def __init__(self, enableBars = False, **kwargs):
		super(TemperatureSimulation, self).__init__(enableBars, **kwargs);
		self.temps = kwargs["temps"];
		self.measPerTemp = {};
		self.ensPerTemp = {};

	def run(self, theory, algo):
		if self.mode == "measurements":
			for t in temps:
				theory.coldStart();
				theory.action.beta = 1/t;
			self.measPerTemp[t] = super(TemperatureSimulation, self).run(theory, algo);
			return self.measPerTemp;
		elif self.mode == "ensemble":
			for t in temps:
				theory.coldStart();
				theory.action.beta = 1/t;
			self.ensPerTemp[t] = super(TemperatureSimulation, self).run(theory, algo);
			return self.ensPerTemp;
		else:
			for t in temps:
				theory.coldStart();
				theory.action.beta = 1./t;
			out = super(TemperatureSimulation, self).run(theory, algo);
			self.ensPerTemp[t] = out["ensemble"];
			self.measPerTemp[t] = out["measurements"];
			return {"ensemble": self.ensPerTemp, "measurements": self.measPerTemp};


#not sure how to make this.........
class InstantSimulation(Simulation):
	def __init__(self, **kwargs):
		kwargs["corSweeps"] = 1;
		kwargs["thermTime"] = 0;
		super(InstantSimulation, self).__init__(False, **kwargs);
	#no need to thermalize in an instant sim
	def thermalize(self, theory, algo):
		pass;