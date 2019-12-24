import numpy
import cmath
import itertools as it

class FourierAcceleration2D:
	def __init__(self):
		pass;

	def update(self, theory):
		dims = theory.field.dims;
		a = theory.action.a;
		momLat = numpy.zeros(dims, dtype = complex);
		dims1End = dims[1]//2 + 1;#correct for odd
		for i, j in it.product(range(dims[0]), range(dims1End)):
			if (i,j) <= (dims[0]//2, dims[1]//2):
				mom = (i,j);
			elif i <= dims[0]//2 and j > dims[1]//2:
				mom = (i, j-dims[1]);
			elif i > dims[0]//2 and j <= dims[1]//2:
				mom = (i-dims[0], j);
			else:
				mom = (i-dims[0], j-dims[1]);
			real = numpy.random.normal(loc = 0, scale = numpy.sqrt(len(theory.field)/(a**(len(dims)))*theory.action.prop(theory.field, mom)));
			imag = numpy.random.normal(loc = 0, scale = numpy.sqrt(len(theory.field)/(a**(len(dims)))*theory.action.prop(theory.field, mom)));
			#try dividing things by sqrt(2): works, BUT WHY???
			if (i,j) == (0,0):
				momLat[(i,j)] = numpy.complex(real, 0);
			elif (i,j) == (dims[0]-i, dims[1]-j) or ((i,j) == (0, dims[1] - j)) or ((i,j) == (dims[0] - i, 0)):
				momLat[(i,j)] = numpy.complex(real, 0);
			else:
				momLat[(i,j)] = numpy.complex(real, imag)/numpy.sqrt(2);
			momLat[((dims[0]-i)%dims[0], (dims[1]-j)%dims[1])] = numpy.conjugate(momLat[(i,j)]);
		newLat = numpy.fft.fftn(momLat)/len(theory.field);
		newLat = numpy.real(newLat);
		theory.field.fromNumpy(newLat);

class RandomGaussians:
	def __init__(**kwargs):
		self.width = kwargs["width"];
		self.mean = kwargs["mean"];

	def update(self, theory):
		newLat = numpy.random.uniform(loc = self.mean, width = self.width, size = theory.field.dims);
		theory.field.fromNumpy(newLat);