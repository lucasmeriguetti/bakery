import maya.cmds as cmds
import lmutils.timeline as timeline
import bakery.baker as baker

def nparticle_locators(selection):

	n_locator_offsets = []
	n_locators = []
	n_particles = []
	nucleus = None

	for index, transform in enumerate(selection):
		print transform
		init_pos = cmds.xform(transform, query = True, translation = True, ws = True)
			
		n_particle = cmds.nParticle(p = init_pos, name = "particle_{}_{}".format(transform, index))

		n_locator_offset = cmds.createNode("transform", name = 'n_locator_offset_{}'.format(index))

		n_locator = cmds.spaceLocator(name = 'n_locator_{}'.format(index))

		cmds.parent(n_locator, n_locator_offset)


		nucleus = cmds.listConnections("{}.startFrame".format(n_particle[1])
			, source = True, type = 'nucleus', scn = True)
		
		cmds.setAttr("{}.gravity".format(nucleus[0]), 0)
		cmds.setAttr("{}.particleRenderType".format(n_particle[1]), 3)
		cmds.goal(n_particle[1], goal = transform, utr = True)
		
		cmds.connectAttr("{}.worldCentroid".format(n_particle[1]),"{}.translate".format(n_locator_offset))

		n_locator_offsets.append(n_locator_offset)
		n_locators.append(n_locator[0])
		n_particles.append(n_particle[0])

	setup_group = cmds.createNode('transform', name = 'setup_group')

	cmds.parent(n_locator_offsets, n_particles, nucleus, setup_group)
	
	return n_locator_offsets, n_particles, nucleus, setup_group, n_locators

def rig(selection):
	cmds.currentTime(timeline.get()[0])
	parents = []
	for node in selection:
		parents.extend(cmds.listRelatives(node, parent = True))

	n_locator_offsets, n_particles, nucleus, setup_group, n_locators = (nparticle_locators(parents))

	for node, n_locator in zip(selection, n_locators):
		cmds.pointConstraint(n_locator, node)

def bake(selection):
	cmds.currentTime(timeline.get()[0])

	locators = baker.create_locators(selection)
	n_locator_offsets, n_particles, nucleus, setup_group, n_locators = (nparticle_locators(locators))

	for locator,node in zip(n_locators, selection):
		cmds.pointConstraint(locator, node)

	physics_group = cmds.createNode('transform', name = 'physics_group')
	cmds.parent(setup_group, locators, physics_group)