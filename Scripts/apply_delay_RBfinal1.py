# function x_delayed = apply_delay(x, delay_s, srate);
# applies arbitrary delay to signal X. The delay does
# not have to be a multiple of the sampling frequency.
# argument delay_s specified in seconds.

def apply_delay(   x, delay_s,  srate ):
    import numpy


    odd_flag = 0
    n = length(x)
    if n%2 == 1:     # ensure that there are an even number of points
        x[n] = numpy.empty()
        n = n-1
        odd_flag = 1   # will add a point at the end so the two will be same length


    n2 = n/2     # half of n

    # make a frequency vector
    fr = numpy.array(1,n2)
    freq = numpy.transpose(fr) / (n2 * (srate/2))

    # get required phase shift vector
    phase_shift = -2*pi*freq(1,n2-1)*delay_s  # skip highest freq comp.

    # apply fft
    X = numpy.fft(x)

    # shift the positive frequencies
    X[2,n2] = X(2,n2) * exp(i*phase_shift)

    # shift the negative frequencies
    X[n2+2,end] = X(n2+2,end) * exp(-i*phase_shift[ ::-1]) # a(end:-1:1,: -> a[ ::-1,:]

# get the delayed waveform
    x_delayed = numpy.fft.ifft(X)
    if odd_flag == 1:
        x_delayed = [x_delayed.append(x_delayed(end))]    # tack on a point to make odd again


    return x_delayed
