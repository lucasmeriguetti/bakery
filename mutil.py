import maya.cmds as cmds

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