import numpy as np


# wrap list as numpy array
def asarray(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return np.array(result)
    return wrapper

def constant(func):
    def fset(self, value):
        raise TypeError("Constant - no setting!")
    def fget(self):
        return func(self)
    return property(fget, fset)