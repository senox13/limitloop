from time import perf_counter, sleep
import math, threading

"""
limitloop.py is a simple module for running loops that need to be run at a
consistant, limited speed
"""

__all__ = ['limitloop', 'endloop', 'getfps']

#Globals
DEFAULT_FPS_LIMIT = 30 #Equivalent to hz

#Module vars
_running = False
_fps = 0
_fps_limit = DEFAULT_FPS_LIMIT
_frame_start_time = 0

def limitloop(function, fps_limit=DEFAULT_FPS_LIMIT, *args, **kwargs):
    """
    Calls the supplied function as fast as possible, up to the number of times
    per second specified in fps_limit. args and kwargs, if provided, are
    passed to the called function
    
    :param function: The function or callable to call every frame
    :param fps_limit: The maximum number of times per second to call the callable specified in function
    :returns: The value returned by the last call to function, or None
    """
    global _running
    global _fps
    global _frame_start_time
    global _fps_limit
    _running = True
    _fps_limit = fps_limit
    target_frame_time = 1/fps_limit
    retval = None
    while _running: #Main loop
        _frame_start_time = perf_counter() #Get start time
        retval = function(*args, **kwargs) #Call function and save returned value
        time_taken = perf_counter() - _frame_start_time #Find time elapsed
        _fps = min(1/time_taken, fps_limit) #Calculate FPS based on how long this frame took
        if(time_taken < target_frame_time): #If no sleep is needed, just continue
            sleep(target_frame_time - time_taken) #Sleep for remaining time
    return retval #Return last returned value

def endloop():
    """After the frame that this is called during has completed, exit loop"""
    global _running
    _running = False

def getfps():
    """Return the semi-instantaneous FPS as defined by 1 divided by the time the last frame took"""
    global _fps
    return _fps

def frame_time_remaining():
    """Return the time in seconds left in this frame to maintain framerate, as a float"""
    global _frame_start_time
    global _fps_limit
    curr_time = perf_counter()
    time_taken = curr_time - _frame_start_time
    target_frame_time = 1/_fps_limit
    remaining = target_frame_time - time_taken
    return remaining

