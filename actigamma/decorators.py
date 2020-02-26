import numpy as np


# wrap list as numpy array
def asarray(func):
    """
        Decorator to wrap a function that returns
        a list to a numpy array.
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return np.array(result)
    return wrapper

# sort a list - something wrong with this
def sortresult(func):
    """
        Decorator to wrap a function that returns
        a list to return a sorted list.
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return sorted(result)
    return wrapper

def constant(func):
    """
        Decorator that prevents a value from being changed.
        Represents a constant as best as possible.
    """
    def fset(self, value):
        raise TypeError("Constant - no setting!")

    def fget(self):
        return func(self)
    return property(fget, fset)
