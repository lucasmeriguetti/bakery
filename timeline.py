import maya.cmds as cmds 

def set(start, end):
	cmds.playbackOptions(min = start, max = end)
	return (start, end)

def get():
	start = cmds.playbackOptions(query = True, min = True)
	end = cmds.playbackOptions(query = True,  max = True)
	return (start, end)

def get_slider():
	aPlayBackSlider= maya.mel.eval('$tmpVar=$gPlayBackSlider')

	if not cmds.timeControl(aPlayBackSlider, query = True, rangeVisible = True):
		return cmds.warning("No range selected")

	time_slider_range = cmds.timeControl(aPlayBackSlider, query = True, rangeArray = True)
	timeline_range =  tuple(time_slider_range)
	return timeline_range
			