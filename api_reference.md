# __Limitloop documentation__

## Available Types

#### `class limitloop.Loop`
A class for calling a single function repeatedly with precise timing

## Loop objects
A Loop instance represents a function, the frequency with with to call it, and provides accessor functions for the functions arguments and return value.

#### `class Loop(func, freq=30, saveArgs=False)`
*func* is the function to repeatedly call. The calling `Loop` instance will pass itself to this function as the first argument.  
*freq* is the number of times per second that *func* should be called.  

#### `Loop.running`
True if the loop is currently running, False if it is halted. Note that the current iteration will still complete before the loop fully ends. This property is read-only.

#### `Loop.frequency`
Determines how many times per second the function should be called. Note that if the function takes longer than `1/frequency` seconds to execute, the next call will be delayed. This can be avoided by having the function check `Loop.frameTime()` and compare it to `Loop.targetTime()` so that it can return early if it is exceeding the target time. Raises a RuntimeError if called while `Loop.running` is True.

#### `Loop.saveArgs`
Determines the behavior of `Loop.setArgs()`. If set to true, arguments will persist between iterations. When false (default), arguments are only passed to the next call to the function. Setting this property will raise a RuntimeError if the loop is running.

#### `Loop.run(count=-1)`
Starts the timed loop executing. *count* determines how many times the loop will be allowed to run before automatically ending. If *count* is less than 0, the loop will run infinitely. Raises a RuntimeError if the loop is already running. Looping stops when `Loop.end()` is called.

#### `Loop.end()`
Stops the timed loop. Raises a RuntimeError if the loop is not running.

#### `Loop.frameTime()`
Returns the time, in seconds, that have elapsed so far on this iteration of the loop. Raises a RuntimeError if the loop is not running.

#### `Loop.targetTime()`
Returns the target amount of time, in seconds, between loop iterations.

#### `Loop.framesPerSecond()`
Returns the estimated instantaneous FPS of the loop, based on how long the last frame took. Returns 0 if called while the loop is not running.

#### `Loop.setArgs(*args, **kwargs)`
Sets the arguments that will be passed to the function. If *saveArgs* was set to True in the constructor, these args will be passed to all subsequent calls of the function.

#### `Loop.lastReturn()`
Returns the value that was returned by the last call to this `Loop` instance's function.
