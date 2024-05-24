#!/usr/bin/env python3
import coverage, unittest, time, sys, os
from time import perf_counter
try:
    from limitloop import *
except ImportError:
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
    def testRunTimeDrift(self): #This does not pass. There is time drift and it's fairly significant
        runForSeconds = 3
        self.loop.frequency = 600
        startTime = perf_counter()
        self.loop.run(self.loop.frequency * runForSeconds)
        endTime = perf_counter()
        timeMs = (endTime - startTime) * 1000
        self.assertLess(timeMs, TIMING_THRESHOLD)
    
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
    
    #Loop.frameTime tests
    def testFrameTime(self):
        def testFunc(loopObj):
            self.assertLess(loopObj.frameTime(), loopObj.targetTime())
            loopObj.end()
        self.loop = Loop(testFunc)
        self.loop.run()
    
    def testFrameTimeRuntimeError(self):
        self.assertRaises(RuntimeError, self.loop.frameTime)
    
    #Loop.targetTime tests
    def testTargetTime(self):
        self.assertEqual(self.loop.targetTime(), 1/30)
    
    #Loop.framesPerSecond tests
    def testFramesPerSecond(self):
        self.firstRun = True
        def testFunc(loopObj):
            if not self.firstRun: #framesPerSecond always returns 0 on first frame
                self.assertEqual(loopObj.framesPerSecond(), 30)
                loopObj.end()
            else:
                self.firstRun = False
        self.loop = Loop(testFunc, saveArgs=False)
        self.loop.run()
    
    #Loop.setArgs and Loop.saveArgs tests
    def testSetArgsSaveArgsTrue(self):
        def testFunc(loopObj, val=0):
            self.assertEqual(val, 10)
        self.loop = Loop(testFunc, saveArgs=True)
        self.loop.setArgs(10)
        self.loop.run(5)
    
    def testSetArgsSaveArgsFalse(self):
        self.firstRun = True
        def testFunc(loopObj, val=0):
            if self.firstRun:
                self.assertEqual(val, 10)
                self.firstRun = False
            else:
                self.assertEqual(val, 0)
                loopObj.end()
        self.loop = Loop(testFunc, saveArgs=False)
        self.loop.setArgs(val=10)
        self.loop.run()
    
    def testGetSaveArgs(self):
        var = self.loop.saveArgs
        self.assertEqual(var, self.loop.saveArgs)
    
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
