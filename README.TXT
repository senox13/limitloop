All documentation copied directly out of docstrings

limitloop.py is a simple module for running loops that need to be run at a consistant, limited speed

Functions:

limitloop(function, fps_limit=DEFAULT_FPS_LIMIT, *args, **kwargs):
    Calls the supplied function as fast as possible, up to the number of times
    per second specified in fps_limit. args and kwargs, if provided, are
    passed to the called function
    
    :param function: The function or callable to call every frame
    :param fps_limit: The maximum number of times per second to call the callable specified in function
    :returns: The value returned by the last call to function, or None

endloop():
    After the frame that this is called during has completed, exit loop

getfps():
    Return the semi-instantaneous FPS as defined by 1 divided by the time the last frame took

def frame_time_remaining():
    Return the time in seconds left in this frame to maintain framerate, as a float

