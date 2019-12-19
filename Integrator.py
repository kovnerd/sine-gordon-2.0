import Scheduler as SCHED
#would like to replace site.value with site?


class Integrator:
	def __init__(self, G,  **kwargs):
		if kwargs["intType"] == "euler":
			self.integrator = Euler(G, kwargs["indices"], kwargs["nSteps"], kwargs["stepSize"]);
		elif kwargs["intType"] == "leapfrog":
			self.integrator = LeapFrog(G, kwargs["indices"], kwargs["isEven"], kwargs["nSteps"], kwargs["stepSize"]);
		else:
			print("specify Integrator type");
			#fail somehow

	def loop(self):
		return self.integrator.loop();

	def step(self, lat):
		self.integrator.step(lat);

	def integrate(self, lat):
		self.integrator.integrate(lat);





class Euler: #default is Euler:
	def __init__(self, G, indices, nSteps, stepSize):
		self.G = G;
		self.indices = indices;
		self.nSteps = nSteps;
		self.stepSize = stepSize;

	def loop(self):
		return self.indices;

	def step(self, lat):
		for index in self.indices:
			lat[index] += self.stepSize*self.G(lat[index]);

	def integrate(self,lat):
		for i in range(self.nSteps):
			self.step(lat);



class LeapFrog:
	def __init__(self, G, indices, isEven, nSteps, stepSize):
		self.G = G;
		self.indices = SCHED.EvenOdd(indices, isEven);
		self.nSteps = nSteps;
		self.stepSize = stepSize;

	def loop(self):
		return self.indices.even;

	def step(self, lat):
		for index in self.loop():
			lat[index] += self.stepSize*self.G(lat[index]); #hopefully += gets defined well...

	def integrate(self, lat):
		#do first half step on even
		self.stepSize *= 0.5;
		self.step(lat);
		self.stepSize *= 2.;
		#do nSteps-1 full steps
		for i in range(self.nSteps):
			self.indices.even, self.indices.odd = self.indices.odd, self.indices.even;#update odd
			self.step(lat);
			self.indices.even, self.indices.odd = self.indices.odd, self.indices.even;#update even
			self.step(lat);
		#do second half step
		self.indices.even, self.indices.odd = self.indices.odd, self.indices.even;#update odd	
		self.stepSize *= 0.5;
		self.step(lat);
		self.stepSize *= 2.;
