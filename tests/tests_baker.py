import bakery.baker as baker
reload(baker)
import maya.cmds 

class TestBaker(unittest.TestCase):
	def setUp(self):
		self.bakerObject = baker.Baker()

	def tearDown(self):
		cmds.delete(self.bakerObject.getSet())


	def test_createBakerNode(self):
		self.bakerObject.createBakerSet()
		result = cmds.objExists(self.bakerObject.getSet())
		self.assertTrue(result)

	def test_addAttrToBakerSet(self):
		self.bakerObject.createBakerSet()
		self.bakerObject.addAttrSet()
		result = cmds.attributeQuery("bakerSet",
			node = self.bakerObject.getSet(),exists = True)
		self.assertTrue(result)


def runTests():	
	print("\n TEST BAKER")
	testCases = [TestBaker]
	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner(verbosity = 2).run(suite)


if __name__ == "__main__":
	runTests()

