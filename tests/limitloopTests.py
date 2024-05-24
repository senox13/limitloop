#!/usr/bin/env python3
import coverage, unittest, time, sys, os
sys.path.append('..')
from limitloop import *

#Any deviation from optimal timing by grater than this many MS will trigger an error
TIMING_THRESHOLD = 1

class LoopTests(unittest.TestCase):
    def setUp(self):
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
    
    #Loop.frequency tests
    def testGetDefaultFrequency(self):
        self.assertEqual(self.loop.frequency, 30)
    
    def testDefaultFrequencyTiming(self):
        callTimes = []
        def testFunc(loopObj):
            callTimes.append(time.perf_counter())
        self.loop = Loop(testFunc)
        self.loop.run(30) #~1 second
        diffTimes = []
        last = None
        for t in callTimes:
            if not last:
                last = t
                continue
            diffTime = (t-last) * 1000 - 33
            diffTimes.append(diffTime)
            last = t
        self.assertLess(max(diffTimes), TIMING_THRESHOLD)
    
    def testSetFrequency(self):
        callTimes = []
        def testFunc(loopObj):
            callTimes.append(time.perf_counter())
        self.loop = Loop(testFunc)
        self.loop.frequency = 100 #~10ms apart
        self.loop.run(100) #~1 second
        diffTimes = []
        last = None
        for t in callTimes:
            if not last:
                last = t
                continue
            diffTime = (t-last) * 1000 - 10
            diffTimes.append(diffTime)
            last = t
        self.assertLess(max(diffTimes), TIMING_THRESHOLD)
    
    def testSetFrequencyRuntimeError(self):
        def testFunc(loopObj):
            loopObj.frequency = 10
        self.loop = Loop(testFunc)
        self.assertRaises(RuntimeError, self.loop.run)
    
    #Loop.run and Loop.end tests
        #testRunInfinite
        
        #testRunTimeDrift
    
    def testRunAndEnd(self):
        def testFunc(loopObj):
            loopObj.end()
        self.loop = Loop(testFunc)
        self.loop.run()
        
    def testRunRuntimeError(self):
        def testFunc(loopObj):
            self.assertRaises(RuntimeError, loopObj.run)
            loopObj.end()
        self.loop = Loop(testFunc)
        self.loop.run()
    
    def testEndRuntimeError(self):
        self.assertRaises(RuntimeError, self.loop.end)
    
    #Loop.frameTime tests #TODO
        #testFrameTime
        
    def testFrameTimeRuntimeError(self):
        self.assertRaises(RuntimeError, self.loop.frameTime)
    
    #Loop.targetTime tests
    def testTargetTime(self):
        self.assertEqual(self.loop.targetTime(), 1/30)
    
    #Loop.framesPerSecond tests
        #testFramesPerSecond
    
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
                self.assertEqual(val, 10)
            else:
                self.assertEqual(val, 0)
        self.loop = Loop(testFunc, saveArgs=False)
        self.loop.setArgs(10, True)
        self.loop.run(5)
    
    #testGetSaveArgs
    
    def testSetSaveArgs(self):
        def testFunc(loopObj, value=0):
            self.assertEqual(value, 10)
        self.loop = Loop(testFunc)
        self.loop.saveArgs = True
        self.loop.setArgs(value=10)
        self.loop.run(5)
    
    def testSetSaveArgsRuntimeError(self):
        def testFunc(loopObj):
            loopObj.saveArgs = True
        self.loop = Loop(testFunc)
        self.assertRaises(RuntimeError, self.loop.run)
    
    #Loop.lastReturn tests
    def testLastReturn(self):
        def testFunc(loopObj):
            loopObj.end()
            return 10
        self.loop = Loop(testFunc)
        self.loop.run()
        self.assertEqual(self.loop.lastReturn(), 10)

if __name__ == "__main__":
    unittest.main()
