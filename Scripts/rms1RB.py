def rms1(x):
    import numpy
# function to return rms voltage of an array x
    x2=x**2
    power=numpy.mean(x2)
    vrms=numpy.sqrt(power)
    return vrms
