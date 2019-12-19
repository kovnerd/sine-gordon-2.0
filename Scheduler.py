import numpy;

#redo these in terms of actual queue's...


class Explicit: #basically a container wrapper class...
	def __init__(self, container):
		self.items = container;	
		self.current = 0;
	def next(self):
		nextItem = self.items[self.current];
		if self.current == len(self.items)-1:
			self.current = 0;
		else:
			self.current += 1;
		return nextItem;

class Random:
	def __init__(self, items):
		self.items = items;
	def next(self):
		current = self.items[0];
		rand = numpy.random.randint(0, len(self.items));
		nextitem = self.items[rand];
		self.items[0] = nextitem;
		self.items[rand] = current;
		return nextitem;

class EvenOdd(Explicit):
	def __init__(self, container, isEven): #isEven is a function that determines if item is even
		#sort into even and odd here
		self.even = [];
		self.odd = [];
		for item in container:
			if isEven(item):
				self.even.append(item);
			else:
				self.odd.append(item);
		self.items = self.even + self.odd;
	def next(self): #change to looping through evens, then odds
		super(EvenOdd, self).next();

	def switch(self):
		even, odd = odd, even;
