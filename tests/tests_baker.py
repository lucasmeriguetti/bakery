import bakery.baker as baker
import unittest
reload(baker)
import maya.cmds 

class TestBaker(unittest.TestCase):
	def setUp(self):
		self.bakerObject = baker.Baker()

	def tearDown(self):
		cmds.delete(self.bakerObject.getBakerSet())

		if len(cmds.ls(tr = True, ud = False)) > 0:
			cmds.delete(cmds.ls(tr = True, ud = False))

		baker.Baker.setIndex(0)


	def test_createBakerSet(self):
		self.bakerObject.createBakerSet()
		result = cmds.objExists(self.bakerObject.getBakerSet())
		self.assertTrue(result)

	def test_addAttrToBakerSet(self):
		self.bakerObject.createBakerSet()
		self.bakerObject.addAttrBakerSet(self.bakerObject.getBakerSet())
		result = cmds.attributeQuery("bakerSet",
			node = self.bakerObject.getBakerSet(),exists = True)
		self.assertTrue(result)

	def test_getBakerSet(self):
		self.bakerObject.createBakerSet()
		result = self.bakerObject.getBakerSet()
		self.assertEqual(result,"BakerSet_0")

	def test_createLocators(self):
		cubes = [cmds.polyCube()[0] for i in range(5)]
		cmds.select(cubes)
		self.bakerObject.run()



def runTests():	
	print("\n TEST BAKER")
	testCases = [TestBaker]
	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner(verbosity = 2).run(suite)


if __name__ == "__main__":
	runTests()

