import maya.cmds as cmds
import bakery.timeline as timeline

import bakery.mutil as mutil

class BaseSets(object):
	def __init__(self):
		self.selection_set_attr = "bakerySelectionSet"  
		self.bakery_elements_set_attr = "bakeryElementsSet" 
		self.bakery_elements_set = None
		self.selection_set = None
		self.locators = []
		self.index = len([i for i in self.get_sets()])

		self.selection = cmds.ls(sl = True)
		if len(self.selection) == 0:
			cmds.warning("Nothing selected. Select at least 1 object.")
			return
			 
	def check_attributes(self, constraint):
		if constraint == "parent":
			mutil.check_locked_attributes(self.selection, 
				translation  =True, rotation = True)
		
		if constraint == "orient":
			mutil.check_locked_attributes(self.selection, 
				translation = False, rotation = True)

	def create_bakery_elements_set(self):
		self.bakery_elements_set = cmds.sets(name = "Bakery_Elements_Set_{}".format(self.index), em = True)
		cmds.addAttr(self.bakery_elements_set, at = "message", 
			longName = self.bakery_elements_set_attr,
			niceName= "Bakery Elements Set")

	def create_selection_set(self):
		self.selection_set = cmds.sets(self.selection, name = "Bakery_Seletion_Set_{}".format(self.index))
		cmds.addAttr(self.selection_set, at = "message", 
			longName = self.selection_set_attr,
			niceName= "Bakery Seletion Set")

	def get_sets(self, attribute_filter = None):
		sets = cmds.ls(sets = True)
		for i in sets:
			attrs = cmds.listAttr(i, st = attribute_filter)
			if attrs:
				yield i

	def bake(self):
		self.bake_elements()
		self.remove_bakery_elements()

	def bake_elements(self):
		bake_elements = []
		time = timeline.get()

		for s in self.get_sets(self.selection_set_attr):
			bake_elements.extend(cmds.sets(s, q = True))
		
		bake_elements = list(set(bake_elements))
		cmds.bakeResults(bake_elements, time = time)
		
	def remove_bakery_elements(self):
		cmds.delete([i for i in self.get_sets(self.selection_set_attr)])

		for i in  self.get_sets(self.bakery_elements_set_attr):
			cmds.delete(cmds.sets(i, q = True))

	def add_to_set(self, transforms, set):
		cmds.sets(transforms, edit = True, fe = set)


class Baker(BaseSets):
	def __init__(self, constraint = 'parent', scale_constraint = False):
		super(Baker, self).__init__()

		self.check_attributes(constraint)
		self.create_selection_set()
		self.create_bakery_elements_set()
		self.build(constraint, scale_constraint)



	def create_locators(self, suffix = 'ctrl'):
		euler_filter_attrs = "rx", "ry", "rz"
		time = timeline.get()
		self.locators = []
		constraints = []

		for index, node in enumerate(self.selection):
			locator = cmds.spaceLocator(name = "{}_{}_{}".format(node,suffix,index))[0]
			
			parent = cmds.parentConstraint(node, locator)
			scale =  cmds.scaleConstraint(node, locator)
			constraints.append(parent[0])
			constraints.append(scale[0])
			self.locators.append(locator)

		cmds.bakeResults(self.locators, time = time)

		for locator in self.locators:
			for attr in euler_filter_attrs:
				cmds.filterCurve("{}.{}".format(locator, attr))

		cmds.delete(constraints)

		self.add_to_set(self.locators, self.bakery_elements_set)

	def constraint_nodes(self, constraint = 'parent', scale_constraint = False):
		for node, locator in zip(self.selection, self.locators):
			try:
				if constraint == 'parent':
					cmds.parentConstraint(locator, node, mo = True)

				elif constraint == 'point': 
					cmds.pointConstraint(locator, node, mo = True)

				elif constraint == 'orient': 
					cmds.orientConstraint(locator, node, mo = True)
				
				
				if scale_constraint:
						cmds.cutKey(node, cl = True, at = ("sx","sy","sz"))
						cmds.scaleConstraint(locator, node, mo = True)
			
			except Exception as e:
				Warning(e)

	def build(self, constraint = 'parent', scale_constraint = False):
		self.create_locators()
		self.constraint_nodes(constraint = constraint, scale_constraint = scale_constraint)


class Layer():
	pass

def create_locators(selection, suffix = 'ctrl'):
	euler_filter_attrs = "rx", "ry", "rz"
	time = timeline.get()
	locators = []
	constraints = []

	for index, node in enumerate(selection):
		locator = cmds.spaceLocator(name = "{}_{}_{}".format(node,suffix,index))[0]
		
		parent = cmds.parentConstraint(node, locator)
		scale =  cmds.scaleConstraint(node, locator)
		constraints.append(parent[0])
		constraints.append(scale[0])
		locators.append(locator)

	cmds.bakeResults(locators, time = time)

	for locator in locators:
		for attr in euler_filter_attrs:
			cmds.filterCurve("{}.{}".format(locator, attr))

	cmds.delete(constraints)

	return locators 
	   
def constraint_nodes(locators, selection, constraint = 'parent', scale_constraint = False):
	for node, locator in zip(selection, locators):
		try:
			if constraint == 'parent':
				cmds.parentConstraint(locator, node, mo = True)

			elif constraint == 'point': 
				cmds.pointConstraint(locator, node, mo = True)

			elif constraint == 'orient': 
				cmds.orientConstraint(locator, node, mo = True)
			
			
			if scale_constraint:
					cmds.cutKey(node, cl = True, at = ("sx","sy","sz"))
					cmds.scaleConstraint(locator, node, mo = True)
		
		except Exception as e:
			Warning(e)

def build(constraint = 'parent', scale_constraint = False):
	selection = cmds.ls(sl = True)

	if constraint == "parent":
		mutil.check_locked_attributes(selection, translation  =True, rotation = True)
	
	if constraint == "orient":
		mutil.check_locked_attributes(selection, translation = False, rotation = True)

	locators = create_locators(selection)
	constraint_nodes(locators, selection, constraint = constraint, scale_constraint = scale_constraint)

	return locators 

if __name__ == "__main__":
	build()