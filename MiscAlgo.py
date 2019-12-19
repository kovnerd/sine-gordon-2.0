import numpy
import cmath
import itertools as it

class FourierAcceleration2D:
	def __init__(self):
		pass;

	#ENFORCES HERMITIAN SYMMETRY -> GENERATES REAL POS-SPACE FIELDS CORRECTLY
	def update(self, theory):
		dims = theory.field.dims;
		momLat = numpy.zeros(dims, dtype = complex);
		dims1End = dims[1]//2 + 1;
		'''
		if (dims[1] % 2 == 0):
			dims1End = dims[1]//2 + 2;
		else:
			dims1End = dims[1]//2 + 1;
		'''
		for i, j in it.product(range(dims[0]), range(dims1End)):
			#correct version 
			#WORKS FOR ODD LENGTHS, NOT EVEN LENGTHS
			#add extra check at boundary: if (i,j) < (dims[0]//2, dims[1]//2) do the other one???
			if (i,j) <= (dims[0]//2, dims[1]//2):
				mom = (i,j);
			elif i <= dims[0]//2 and j > dims[1]//2:
				mom = (i, j-dims[1]);
			elif i > dims[0]//2 and j <= dims[1]//2:
				mom = (i-dims[0], j);
			else:
				mom = (i-dims[0], j-dims[1]);
				
			real = numpy.random.normal(loc = 0, scale = numpy.sqrt(theory.action.prop(theory.field, mom)));
			imag = numpy.random.normal(loc = 0, scale = numpy.sqrt(theory.action.prop(theory.field, mom)));
			
			#enforce hermitian symmetry
			if (i,j) == (0,0) or (i,j) == (dims[0]-i, dims[1]-j):
				momLat[(i,j)] = numpy.complex(real, 0);
			else:
				momLat[(i,j)] = numpy.complex(real, imag);
				if i == 0 and j != 0: # first row leg
					if j == dims[1] - j:
						momLat[(i, j)] = numpy.complex(real, 0);
					else:
						momLat[(i, dims[1] - j)] = numpy.conjugate(momLat[(i,j)]);
				elif i !=0 and j == 0: # vertical leg
					if i == dims[0] - i:
						momLat[(i, j)] = numpy.complex(real, 0);#make b[i,j] real
					else:
						momLat[(dims[0] - i, j)] = numpy.conjugate(momLat[(i, j)]); 
				else: #body
					momLat[(dims[0] - i, dims[1] - j)] = numpy.conjugate(momLat[(i, j)]); 
		
		newLat = numpy.fft.ifftn(momLat);
		#print("imaginary part (should be 0's): \n" + str(numpy.imag(newLat)));
		#print(newLat);
		newLat = numpy.real(newLat);
		#print(newLat.shape);
		theory.field.fromNumpy(newLat);

class RandomGaussians:
	def __init__(**kwargs):
		self.width = kwargs["width"];
		self.mean = kwargs["mean"];

	def update(self, theory):
		newLat = numpy.random.uniform(loc = self.mean, width = self.width, size = theory.field.dims);
		theory.field.fromNumpy(newLat);