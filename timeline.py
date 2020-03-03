import maya.cmds as cmds 
def set(start, end):
	cmds.playbackOptions(animationStartTime = start, animationEndTime = end)
	return (start, end)

def get():
	start = cmds.playbackOptions(query = True, min = True)
	end = cmds.playbackOptions(query = True,  max = True)
	return (start, end)

def get_slider():
		
	try:
		aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
		time_slider_range = cmds.timeControl(aPlayBackSliderPython, query = True, rangeArray = True)
		timeline_range =  tuple(time_slider_range)
		return timeline_range
			
	except:
		print ("You have to select a time range.")
		return (start, end)