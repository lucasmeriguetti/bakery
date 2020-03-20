import bakery.baker as baker
import unittest
reload(baker)
import maya.cmds 

class TestBaker(unittest.TestCase):
	def setUp(self):
		cmds.delete(cmds.ls(tr = True, 
	 		sets = True, visible = True, 
	 		ud = False, undeletable = False))

		baker.Baker.setIndex(0)
		self.bakerObject = baker.Baker()

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
		print "CREATE LOCATORS "
		baker.Baker.setIndex(0)
		cubes = [cmds.polyCube()[0] for i in range(5)]
		cmds.select(cubes)

		bakerObject = baker.Baker()
		bakerObject.run()
		setObject = bakerObject.getBakerSet()

def runTests():	
	print("\n TEST BAKER")
	testCases = [TestBaker]
	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner(verbosity = 2).run(suite)


if __name__ == "__main__":
	runTests()

