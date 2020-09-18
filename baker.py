import maya.cmds as cmds
import bakery.timeline as timeline
class Baker(object):
	def __init__(self, name = None, selection = None):
		self.sets_attr = "bakingSet"
		
		self.selection = selection
		if not self.selection:
			self.selection = cmds.ls(sl = True)

	def create_set(self):
		bset = cmds.sets(self.selection)
		cmds.addAttr(bset, at = "message", 
			longName = self.sets_attr,
			niceName= "Baking Set")

	def get_sets(self):
		sets = cmds.ls(sets = True)
		for i in sets:
			attrs = cmds.listAttr(st = self.sets_attr)
			if self.sets_attr in attrs:
				yield i

	def bake_from_set(self, setname):
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
							message = "Someone locked the freaking attributes!!!\nScript won't run!!!")

						raise Exception("Locked Attributes: {}".format(locked_attributes))


	return False

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

	return locators 

if __name__ == "__main__":

	build()