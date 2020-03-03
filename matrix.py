import maya.cmds as cmds

class Matrix4():
	def __init__(self, transform, space = "world"):
		self.__transform = transform
		self.__space = space

		self.__row_index = 0
		self.__column_index = 0

		self.x = [1,0,0,0]
		self.y = [0,1,0,0]
		self.z = [0,0,1,0]
		self.w = [0,0,0,1] 

		self.__matrix =[self.x, 
				   	 	self.y,
				   	 	self.z,
				     	self.w]

		self.build()

	def build(self):
		if self.__space == "object":
			os = True
			ws = False

		if self.__space == "world":
			os = False 
			ws = True 

		xform_matrix = cmds.xform(	self.__transform, 
									query = True,
									os = os,
									ws = ws,
									matrix = True)
		row = 0
		column = 0
		for i in (xform_matrix):
				
				self.__matrix[column][row] = i
				row += 1
				if row > 3:
						row = 0
						column +=1

	def set_node(self, transform):
		self.__transform = transform 
		self.build()

	def set(self, (row, column), value):
		self.__matrix[row][column] = value
		self.apply_transformation()

	def get(self, (row, column)):
		return self.__matrix[row][column]

	def apply_transformation(self):
		xform_matrix = []
		for row in self.__matrix:
			for element in row:
				xform_matrix.append(element)
		cmds.xform(self.__transform, matrix = xform_matrix, ws = True)

	def iter(self):
		return self

	def next(self):
		self.__row_index = 0
		self.__column_index = 0

		if self.__column_index < 3:
			self.__column_index += 1

		else:
			self.__column_index += 1
			self.__row_index += 1
		
		if self.__row_index > 3:
			raise StopIteration()

	def __getitem__(self, index):
		return self.__matrix[index]

	def __setitem__(self, index, value):
		self.__matrix[index] = value

	def __str__(self):
		title ="- - - - Matrix 4x4 - - - -"
		breaker = "- - - - - - - - - - - - - -"
		return "\n{0}\n{1}, {2} space\n{3}\n{4}\n{5}\n{6}\n{7}\n".format(
				title, 
				self.__transform, 
				self.__space, 
				self.__matrix[0], 
				self.__matrix[1], 
				self.__matrix[2], 
				self.__matrix[3], 
				breaker
				)
