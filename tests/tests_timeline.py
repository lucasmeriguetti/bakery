import maya.cmds as cmds 
import maya.mel 

import bakery.timeline as timeline 
reload(timeline)



class TestTimelineModule(unittest.TestCase):

	def test_get(self):
		start = cmds.playbackOptions(query = True, min = True)
		end = cmds.playbackOptions(query = True,  max = True) 

		timelineRange = timeline.get()
		self.assertEqual(start, timelineRange[0])
		self.assertEqual(end, timelineRange[1])

	def test_set(self):

		timeline.set(start = 0, end = 10)

		timelineRange = timeline.get()
		self.assertEqual(timelineRange, (0,10))


def runTests():	
	print("\n TEST TIMELINE")
	testCases = [TestTimelineModule]
	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner(verbosity = 2).run(suite)


if __name__ == "__main__":
	runTests()

