"""
    A set of utility functions for ActiGamma
"""
from pprint import pprint


# function to plot histogram
def getplotvalues(bounds, binvalues):
    """
        Matplotlib hist is slow. Use a hist like plot with conventional line plot.

        Expects N+1 bounds where len(binvalues) = N
        and returns two arrays both of length 2N to plot as line plot.

        Make sure arrays are of correct length
        len(binvalues) + 1 == len(bounds)

        :param bounds: the X values of the histogram (bounds)
        :param binvalues: the Y values of the histogram (bin values)
        :return: matching length arrays as a tuple
    """
    assert (len(binvalues) + 1) == len(bounds)

    plotbounds, plotvalues = [], []
    for i, value in enumerate(binvalues):
        plotbounds.extend([bounds[i], bounds[i + 1]])
        plotvalues.extend([value, value])

    return plotbounds, plotvalues
