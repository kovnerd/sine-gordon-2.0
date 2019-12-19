from abc import *
import numpy

#may not need this class at all...

class ActionBase(ABC):
	@abstractmethod
	def local(self, localField):
		pass;
	
	@abstractmethod
	def total(self, field):
		pass;
	
	@abstractmethod
	def force(self, localField):
		pass;