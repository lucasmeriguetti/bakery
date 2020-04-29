import maya.cmds as cmds
import maya.api.OpenMaya as om
import bakery.timeline as timeline

class Baker():
	index = 0
	def __init__(self):
		self._selection = None
		self._locators = []
		self._set = None
		self._locatorName = 'locator'
		self._locators = []
	
	def run(self):
		self.createControls()
		self.createBakerSet()
		self.addAttrBakerSet(self._set)
		self.__class__.index += 1

	def createBakerSet(self, name ="BakerSet"):
		self._set = cmds.sets(self._locators, name = "{}_{}".format(name, self.__class__.index))
		
	def addAttrBakerSet(self, node):
		cmds.addAttr(node, at = "message", ln = "bakerSet")

	def getBakerSet(self):
		if not cmds.objExists(self._set):
			cmds.warning("Set doesn't exist.")

		if not cmds.objectType(self._set) == "objectSet":
			cmds.warning("self._set is not of type objectSet.")
			return 
		
		return self._set  

	def getSelection(self):
		self._selection = cmds.ls(sl = True)

	def createControls(self):
		self.getSelection()
 		self._locators = []
		self._constraints = []

 		for i, t in enumerate(self._selection):
 			locator = cmds.spaceLocator(name = '{}_{}_{}'.format(t,self._locatorName, i))[0]
			parent = cmds.parentConstraint(t, locator)
			scale =  cmds.scaleConstraint(t, locator)
			self._constraints.append(parent[0])
			self._constraints.append(scale[0])
			self._locators.append(locator)
			cmds.addAttr(locator, at = "message", ln = "bakerLocator")
	
	def bakeControls(self):
		cmds.bakeResults(self._locators, time = time)
		for locator in self._locators:
			for attr in "rx", "ry", "rz":
				cmds.filterCurve("{}.{}".format(locator, attr))

		cmds.delete(self._constraints)


	def bakeTransforms(self):
		pass 

	def constraintTransforms(self):
		pass 

	def isAttrLocked(self):
		pass 

	def parentConstraint(self):
		pass 

	def orientConstraint(self):
		pass 

	def scaleConstraint(self):
		pass 

	def check_locked_attributes(selection, translation = True, rotation = True):
		translation_attrs = ["translateX", "translateY", "translateZ"]
		rotation_attrs = ["rotateX", "rotateY", "rotateZ"]

		compare_attrs = []

		if translation:
			compare_attrs.extend(translation_attrs)
		
		if rotation:
			compare_attrs.extend(rotation_attrs)

		for node in selection:
			locked_attributes = cmds.listAttr(node, k = True, locked = True)

			if locked_attributes:
				for locked in locked_attributes:
					for compare in compare_attrs:
						if compare == locked:
							cmds.confirmDialog(title = "Locked Attributes",
								message = "Some one locked the freaking attributes!!!\nScript won't run!!!")

							raise Exception("Locked Attributes: {}".format(locked_attributes))

		return False

	@classmethod
	def setIndex(cls, index):
		cls.index = index

def create_locators(selection):
	time = timeline.get()
	locators = []
	constraints = []

	for node in selection:
		locator = cmds.spaceLocator(name = node + '_locator_ctrl_0')[0]
		
		parent = cmds.parentConstraint(node, locator)
		scale =  cmds.scaleConstraint(node, locator)
		constraints.append(parent[0])
		constraints.append(scale[0])
		locators.append(locator)

	cmds.bakeResults(locators, time = time)

	for locator in locators:
		for attr in "rx", "ry", "rz":
			cmds.filterCurve("{}.{}".format(locator, attr))

	cmds.delete(constraints)

	return locators 
	   


def constraint_nodes(locators, selection, constraint = 'parent', scale_constraint = False):
	for node, locator in zip(selection, locators):
		try:
			if constraint == 'parent':
				cmds.parentConstraint(locator, node, mo = True)

			if constraint == 'point': 
				cmds.pointConstraint(locator, node, mo = True)

			if constraint == 'orient': 
				cmds.orientConstraint(locator, node, mo = True)
			
			if scale_constraint:
					cmds.cutKey(node, cl = True, at = ("sx","sy","sz"))
					cmds.scaleConstraint(locator, node, mo = True)
		
		except Exception as e:
			Warning(e)

def build(constraint = 'parent', scale_constrain = False):
	selection = cmds.ls(sl = True)

	if constraint == "parent":
		check_locked_attributes(selection, translation  =True, rotation = True)
	
	if constraint == "orient":
		check_locked_attributes(selection, translation = False, rotation = True)

	locators = create_locators(selection)
	constraint_nodes(locators, selection, constraint = constraint, scale_constraint = scale_constrain)

