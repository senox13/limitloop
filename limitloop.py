from time import perf_counter, sleep
import math

#Globals
DEFAULT_FPS_LIMIT = 30 #Equivalent to hz

#Module vars
_running = False
_fps = 0

def limitloop(function, fps_limit=DEFAULT_FPS_LIMIT, *args, **kwargs):
    """Calls the supplied function with the args passed through *args and **kwargs in a loop, the speed of which is limited to fps_limit"""
    global _running
    global _fps
    _running = True
    target_frame_time = 1/fps_limit
    while _running: #Main loop
        start_time = perf_counter() #Get start time
        function(*args, **kwargs) #Call function
        time_taken = perf_counter() - start_time #Find time elapsed
        _fps = max(time_taken, fps_limit) #Calculate FPS based on how long this frame took
        if(time_taken < target_frame_time): #If no sleep is needed, just continue
            sleep(target_frame_time - time_taken) #Sleep for remaining time

def endloop():
    global _running
    _running = False

def getfps():
    global _fps
    return _fps
