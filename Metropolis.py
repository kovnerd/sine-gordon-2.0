import numpy
import copy


#TO BE COMPATIBLE WITH THIS CLASS, OBJECTS MUST OWN A COPY METHOD THATS NOT copy.copy

class Metropolis:
	def __init__(self, moveScheduler, computeProb):
		self.moves = moveScheduler;
		self.computeProb = computeProb;

	def step(self, current, moveObj):
		old = copy.copy(current);
		moveObj.move(current);
		if(self.computeProb(old, current, moveObj) < numpy.random.uniform()):
			#current.value = old.value;
			current.copy(old); 
			moveObj.rejects+=1;
		else:
			moveObj.accepts+=1;

	#whatever is current is to be defined outside of metropolis: by default a metropolis step = metropolis update
	def update(self, current): 
		self.step(current, self.moves.next());

	def __str__(self):
		output = "";
		acceptTot = rejectTot = 0;
		for item in self.moves.items:#not working...?
			output += str(item);
			acceptTot += item.accepts;
			rejectTot += item.rejects;
		output += "reject/accept = " + str(rejectTot/acceptTot) + "\n";
		return output;


class MetropolisSingleSite(Metropolis):
	def __init__(self, moveScheduler, computeProb):
		super(MetropolisSingleSite, self).__init__(moveScheduler, computeProb);
	
	def update(self, theory):
		for phi_x in theory.field.sites:
			super(MetropolisSingleSite, self).update(phi_x);

#'''
class MetropolisWithOverrelax(MetropolisSingleSite):
	def __init__(self, moveScheduler, computeProb, overrelax):
		super(MetropolisWithOverrelax, self).__init__(moveScheduler, computeProb);
		self.overrelax = overrelax;

	def update(self, theory):
		super(MetropolisWithOverrelax, self).update(theory);
		self.overrelax.move(theory.field);
#'''