from maya import cmds
import bakery.vector as vector
reload(vector)

import bakery.matrix as matrix
reload(matrix)

import bakery.timeline as timeline
reload(timeline)

import bakery.baker as baker
reload(baker)


def create_locators(selection, suffix = "_"):

	locators = []
	
	for index, name in enumerate(selection):
		locator = cmds.spaceLocator(name = ("{}_loc_{}_{}".format(name,index, suffix)))
		cmds.xform(locator, rotateOrder = "yxz")

		cmds.xform(locator, translation = (0,index,0))
		locators.append(locator[0])
	return locators

def create_rig_group(selection, locators, spin_locators):
	rig_group = cmds.createNode('transform', name = "rig_setup")
	cmds.parent(locators, rig_group)
	cmds.parent(spin_locators, rig_group)
	offset_rotation = get_offset_rotation(selection[0])
	cmds.matchTransform(rig_group, selection[0])

	return rig_group

def align(selection, locators, spin_locators):

	node_vector = vector.Vector3().from_transform_translation(selection[0])
	goal_vector = vector.Vector3().from_transform_translation(selection[-1])
	result_vector = goal_vector - node_vector

	distance = result_vector.length()

	for transform, locator, in zip(selection, locators):
		cmds.matchTransform(locator, transform, position = True)

	for index, locator in enumerate(locators[:-1]):
		try:
			aim_axes(locator, locators[index + 1])
			cmds.parent(spin_locators[index], locator)
			cmds.xform(spin_locators[index], translation = (0,0,0), os = True)
			cmds.setAttr("{}.tx".format(spin_locators[index]), distance)
			cmds.parent(spin_locators[index], world = True)

		except:
			print("{} is the end of the chain".format(selection[index]))

	cmds.parent(locators[-1], locators[-2], a = True)
	cmds.xform(locators[-1], os = True, rotation = (0,0,0),)
	cmds.parent(locators[-1], world = True)
	cmds.parent(spin_locators[-1], locators[-1])
	cmds.xform(spin_locators[-1], translation = (0,0,0), rotation = (0,0,0), os = True)
	cmds.setAttr("{}.tx".format(spin_locators[-1]), 10)
	cmds.parent(spin_locators[-1], world = True)


def aim_axes(node, goal):
	
	node_vector = vector.Vector3().from_transform_translation(node)
	goal_vector = vector.Vector3().from_transform_translation(goal)
	result_vector = goal_vector - node_vector
	node_matrix = matrix.Matrix4(node)
	
	v_i = vector.Vector3(result_vector.x, result_vector.y, result_vector.z).normalized()
	node_matrix.set((1,0), v_i.x)
	node_matrix.set((1,1), v_i.y)
	node_matrix.set((1,2), v_i.z)
	
	
	v_j = vector.Vector3(v_i.y, -v_i.x, 0).normalized()
	node_matrix.set((0,0), v_j.x)
	node_matrix.set((0,1), v_j.y)
	node_matrix.set((0,2), v_j.z)
	
	v_w = v_j.cross(v_i)
	
	node_matrix.set((2,0), v_w.x)
	node_matrix.set((2,1), v_w.y)
	node_matrix.set((2,2), v_w.z)
   
def bake(selection, locators, spin_locators):
	constraints = []
	bake_transforms = []
	bake_transforms.extend(locators)
	bake_transforms.extend(spin_locators)

	print bake_transforms

	for transform, locator, spin_locator in zip(selection, locators, spin_locators):
		constraints.append(cmds.parentConstraint(transform, locator, mo = True)[0])
		constraints.append(cmds.parentConstraint(transform, spin_locator, mo = True)[0])

	cmds.bakeResults(bake_transforms, at = ["tx", "ty", "tz"],  time = timeline.get())
	cmds.delete(constraints)

def rig_setup(locators, spin_locators, selection, constraint_type = "parent"):
	cmds.currentTime(timeline.get()[0])
	for index in range(len(locators)):
		try:
			cmds.aimConstraint(locators[index + 1], locators[index],
								mo = True, 
								aim = (0,1,0),
								u = (1,0,0),
								worldUpType = "object",
								wuo = spin_locators[index])
		except:
						cmds.aimConstraint(locators[index - 1], locators[index],
								mo = True, 
								aim = (0,-1,0),
								u = (-1,0,0),
								worldUpType = "object",
								wuo = spin_locators[index])


	for locator, transform in zip(locators, selection):
		if constraint_type == "orient":
			cmds.orientConstraint(locator, transform, mo = True)
		else:
			cmds.parentConstraint(locator, transform, mo = True)

def create_ctrls(locators, spin_locators):
	ctrls = []
	constraints = []
	for index, locator in enumerate(locators):
		ctrl_locator = cmds.spaceLocator(name = "aim_ctrl_{}".format(index))
		ctrls.append(ctrl_locator[0])

		constraints.append(cmds.parentConstraint(locator, ctrl_locator)[0])

	cmds.bakeResults(ctrls, time = timeline.get())

	attrs = []

	for ctrl in ctrls:
		for attr in "rx", "ry", "rz":
			attrs.append("{}.{}".format(ctrl, attr))

	cmds.filterCurve(attrs)


	cmds.delete(constraints)

	for ctrl, locator, spin_locator in zip(ctrls, locators, spin_locators):
		cmds.pointConstraint(ctrl, locator, mo = True)
		cmds.parentConstraint(ctrl, spin_locator, mo = True)

def build(constraint = "parent"):
	selection =  cmds.ls(sl = True)

	if constraint == "parent":
		baker.check_locked_attributes(selection, translation = True, rotation = True)

	if constraint == "orient":
		baker.check_locked_attributes(selection, translation = False, rotation = True)

	cmds.currentTime(timeline.get()[0])

	locators = create_locators(selection, "aim")
	spin_locators = create_locators(selection, "spin")
	
	align(selection, locators, spin_locators)
	bake(selection, locators, spin_locators)
	rig_setup(locators, spin_locators, selection, constraint)
	create_ctrls(locators, spin_locators)
	
	rig_group = cmds.group(locators, spin_locators , name = "aim_setup_0")
	cmds.setAttr(rig_group + ".visibility", 0)
