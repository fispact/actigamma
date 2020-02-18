import numpy as np


# wrap list as numpy array
def asarray(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return np.array(result)
    return wrapper