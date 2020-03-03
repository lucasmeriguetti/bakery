''' Vector stuff '''
import math
import maya.cmds as cmds

#works for vector objects and tuples
def dot_product(v1, v2):
    dot = 0
    for a,b in zip(v1,v2):
        dot += a*b
    
    return (dot) 

def length(v1):
	length = math.sqrt( dot_product(v1, v1) )
	return (length)

def distance(v1, v2):
	v3 = []
	for a,b in zip(v1, v2):
		r = float(a) - b 
		v3.append(r)

	return length(v3)

#vector object
class Vector3():
	def __init__(self, x = 0.0, y = 0.0, z = 0.0):
		self.x = x
		self.y = y
		self.z = z 

		self.__axes = (self.x, self.y, self.z)
		self.__index = 0

	def from_transform_translation(self, transform):
		tx, ty, tz = cmds.xform(transform, translation = True, ws = True, query = True)
		
		return Vector3(tx, ty, tz)

	def axes(self):
		return (self.x, self.y, self.z)

	def dot(self, v2):
		return self.x* v2.x + self.y * v2.y + self.z * v2.z

	def cross(self, v2):
		x = self.y*v2.z - self.z*v2.y
		y = self.z*v2.x - self.x*v2.z 
		z = self.x*v2.y - self.y*v2.x

		return Vector3(x, y, z)

	def length(self):
		return math.sqrt(self.dot(self))

	def normalized(self):
		if self.length() == 0:
			return self
		else:
			return self / self.length()

	def distance(self, v2):
		return (self - v2).length()

	def iter(self):
		return self

	def next(self):
		if self.__index < 2:
			i = self.__index
			self.__index += 1
			return self[i]
		else:
			raise StopIteration()

	def __eq__(self, v2):
		return self.x == v2.x and self.y == v2.y and self.z== v2.z

	def __add__(self, v2):
		x = self.x + v2.x
		y = self.y + v2.y
		z = self.z + v2.z
		return Vector3(x, y, z)

	def __sub__(self, v2):
		x = self.x - v2.x
		y = self.y - v2.y
		z = self.z - v2.z
		return Vector3(x, y, z)

	def __mul__(self, i):
		return Vector3(self.x*i, self.y*i, self.z*i)

	def __div__(self, i):
		return Vector3(self.x/i, self.y/i, self.z/i)

	def __getitem__(self, i):
		return self.__axes[i]

	def __str__(self):
		return "\n- - - Vector 3D - - -\nx: {}\ny: {}\nz: {}\n- - - - - - - - - - - \n".format(self.x, self.y, self.z)