
# function to plot histogram
def getplotvalues(x, y):
    """
        Matplotlib hist is slow. Use a hist like plot with conventional line plot
    """
    assert (len(y) + 1) == len(x)

    X, Y = [], []
    for i, value in enumerate(y):
        X.extend([x[i], x[i+1]])
        Y.extend([value, value])
    
    return X, Y