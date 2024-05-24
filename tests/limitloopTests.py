from limitloop import Loop
import unittest

class LoopTests(unittest.TestCase):
    def setUpClass(self):
        def testFunc(loopObj):
            pass
        self.loop = Loop(testFunc)
    
    #Loop.running tests
    def testGetRunningFalse(self):
        self.assertFalse(self.loop.running)
    
    def testGetRunningTrue(self):
        def testFunc(loopObj):
            self.assertTrue(loopObj.running)
            loopObj.end()
        self.loop = Loop(testFunc)
        self.loop.run()
    
    def testSetRunningAttributeError(self):
        def testFunc():
            self.loop.running = True
        self.assertRaises(AttributeError, testFunc)
    
    #Loop.frequency tests #TODO
        #testDefaultFrequency
    
        #testSetFrequency
    
    def testSetFrequencyRuntimeError(self):
        def testFunc(loopObj):
            loopObj.frequency = 10
        self.loop = Loop(testFunc)
        self.assertRaises(RuntimeError, loopObj.run)
    
    #Loop.run and Loop.end tests
    def testRunAndEnd(self):
        def testFunc(loopObj):
            loopObj.end()
        self.loop = Loop(testFunc)
        self.loop.run()
        
    def testRunRuntimeError():
        def testFunc(loopObj):
            self.assertRaises(RuntimeError, loopObj.run)
        self.loop = Loop(testFunc)
        self.loop.run()
    
    def testEndRuntimeError():
        self.assertRaises(RuntimeError, self.loop.end)
    
    #Loop.frameTime tests #TODO
        #testFrameTime
        
    def testFrameTimeRuntimeError(self):
        self.assertRaises(RuntimeError, self.loop.frameTime)
    
    #Loop.targetTime tests
    def testTargetTime(self):
        self.assertEqual(self.loop.targetTime(), 1/30)
    
    #Loop.setArgs and Loop.saveArgs tests
    def testSetArgsSaveArgsTrue(self):
        def testFunc(loopObj, val=0):
            self.assertEqual(val, 10)
        self.loop = Loop(testFunc, saveArgs=True)
        self.loop.setArgs(10)
        self.loop.run(5)
    
    def testSetArgsSaveArgsFalse(self):
        def testFunc(loopObj, val=0, firstRun=False):
            if firstRun:
                self.assertEqual(val)
            else:
                self.assertEqual(val, 0)
        self.loop = Loop(testFunc, saveArgs=False)
        self.loop.setArgs(10, True)
        self.loop.run(5)
    
    def testSetSaveArgsRuntimeError(self):
        def testFunc(loopObj):
            loopObj.saveArgs = True
        self.loop = Loop(testFunc)
        self.assertRaises(RuntimeError, self.loop.run)
    
    #Loop.lastReturn tests
    def testLastReturn(self):
        def testFunc(loopObj):
            self.assertEqual(loopObj.lastReturn(), 10)
            return 10
        self.loop = Loop(tesFunc)
        self.loop.run()
