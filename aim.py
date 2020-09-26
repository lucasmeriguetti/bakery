from maya import cmds

import bakery.vector as vector
reload(vector)

import bakery.matrix as matrix
reload(matrix)

import bakery.timeline as timeline
reload(timeline)

import bakery.mutil as mutil
reload(mutil)

import bakery.baker as baker
reload(baker)

class AimRig(baker.BaseSets):
	def __init__(self, constraint = "parent"):
		super(AimRig, self).__init__()
		cmds.currentTime(timeline.get()[0])
		self.check_attributes(constraint)
		self.create_selection_set()
		self.create_bakery_elements_set()

		self.build(constraint)

	def create_locators(self,suffix = "_"):
		locators = []
		for index, name in enumerate(self.selection):
			locator = cmds.spaceLocator(name = ("{}_loc_{}_{}".format(name,index, suffix)))
			cmds.xform(locator, rotateOrder = "yxz")

			cmds.xform(locator, translation = (0,index,0))
			locators.append(locator[0])
		
		self.add_to_set(locators, self.bakery_elements_set)
		return locators

	def align_locators(self):

		node_vector = vector.Vector3().from_transform_translation(self.selection[0])
		goal_vector = vector.Vector3().from_transform_translation(self.selection[-1])
		result_vector = goal_vector - node_vector

		distance = result_vector.length()

		for transform, locator, in zip(self.selection, self.aim_locators):
			cmds.matchTransform(locator, transform, position = True)

		for index, locator in enumerate(self.aim_locators[:-1]):
			try:
				self.aim_axes(locator, self.aim_locators[index + 1])
				cmds.parent(self.spin_locators[index], locator)
				cmds.xform(self.spin_locators[index], translation = (0,0,0), os = True)
				cmds.setAttr("{}.tx".format(self.spin_locators[index]), distance)
				cmds.parent(self.spin_locators[index], world = True)

			except:
				print("{} is the end of the chain".format(self.selection[index]))

		cmds.parent(self.aim_locators[-1], self.aim_locators[-2], a = True)
		cmds.xform(self.aim_locators[-1], os = True, rotation = (0,0,0),)
		cmds.parent(self.aim_locators[-1], world = True)
		cmds.parent(self.spin_locators[-1], self.aim_locators[-1])
		cmds.xform(self.spin_locators[-1], translation = (0,0,0), rotation = (0,0,0), os = True)
		cmds.setAttr("{}.tx".format(self.spin_locators[-1]), 10)
		cmds.parent(self.spin_locators[-1], world = True)

	def aim_axes(self, node, goal):
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

	def bake_locators(self):
		constraints = []
		bake_transforms = []
		bake_transforms.extend(self.aim_locators)
		bake_transforms.extend(self.spin_locators)

		for transform, locator, spin_locator in zip(self.selection, 
			self.aim_locators, self.spin_locators):

			constraints.append(cmds.parentConstraint(transform, locator, mo = True)[0])
			constraints.append(cmds.parentConstraint(transform, spin_locator, mo = True)[0])

		cmds.bakeResults(bake_transforms, at = ["tx", "ty", "tz"],  time = timeline.get())
		cmds.delete(constraints)

	def rig_setup(self,constraint = "parent"):
		cmds.currentTime(timeline.get()[0])
		for index in range(len(self.aim_locators)):
			try:
				cmds.aimConstraint(self.aim_locators[index + 1], self.aim_locators[index],
									mo = True, 
									aim = (0,1,0),
									u = (1,0,0),
									worldUpType = "object",
									wuo = self.spin_locators[index])
			except:
							cmds.aimConstraint(self.aim_locators[index - 1], self.aim_locators[index],
									mo = True, 
									aim = (0,-1,0),
									u = (-1,0,0),
									worldUpType = "object",
									wuo = self.spin_locators[index])


		for locator, transform in zip(self.aim_locators, self.selection):
			if constraint == "orient":
				cmds.orientConstraint(locator, transform, mo = True)
			else:
				cmds.parentConstraint(locator, transform, mo = True)
	def create_ctrls(self):
		ctrls = []
		constraints = []
		for index, locator in enumerate(self.aim_locators):
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

		for ctrl, locator, spin_locator in zip(ctrls, self.aim_locators, self.spin_locators):
			cmds.pointConstraint(ctrl, locator, mo = True)
			cmds.parentConstraint(ctrl, spin_locator, mo = True)

		self.add_to_set(ctrls, self.bakery_elements_set)

	def build(self, constraint = "parent"):
		self.aim_locators = self.create_locators("aim")
		self.spin_locators = self.create_locators("spin")
		self.align_locators()
		self.bake_locators()
		self.rig_setup(constraint)
		self.create_ctrls()

		rig_group = cmds.group(self.aim_locators, self.spin_locators , name = "aim_setup_0")
		self.add_to_set([rig_group], self.bakery_elements_set)
		cmds.setAttr(rig_group + ".visibility", 0)