import copy

class Node:
	def __init__(self):
		self.value = 0.;
		self.mu = [];#neighboring nodes
	def __str__(self):
		output = "(val = " + str(self.value) + ", mu = [";#when mu is a reference
		for adj in self.mu:
			output += str(adj.value) + ", ";
		output = output [:-2];
		output += "])";
		return output

	def copy(self, other):#add a safe copy of mu's later
		self.value = other.value;

	def __iadd__(self, other):
		self.value += other.value;

	def __isub__(self, other):
		self.value -= other.value;