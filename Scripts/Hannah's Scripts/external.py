import numpy
import scipy

srate=44100    #sample rate
duration=0.3   #seconds
rise=0.01      #seconds
hipass=100     #high pass filter in Hz
lopass=5000    #low pass filter in Hz
filterorder=8  #filter order

def vrms(x):
    power=numpy.mean(x**2)
    vrms=numpy.sqrt(power)
    return vrms

def signal():
    npts=numpy.round(duration*srate)
    signal = numpy.random.standard_normal((npts,))
   # filter it
    #cutoffs = numpy.array([hipass, lopass])/(srate/2)
    #b, a = numpy.butter(filterorder/2, cutoffs)  #take half of specified filter order, since we're using filtfilt.
   # signal = numpy.filtfilt(b, a, signal)
    return signal

def hanwin(n,npts):
    hann=numpy.hanning(2*npts)
    han1=hann[numpy.arange(1,int(npts))]	# rise portion
    han2=hann[numpy.arange(int(npts)+1,2*int(npts))]	# decay portion

    length=numpy.size(n)
    k1=length-npts+1

    y = n
    y[numpy.arange(1,int(npts))]=y[numpy.arange(1,int(npts))]*han1	#apply rise time
    y[numpy.arange(int(k1),int(length))]=y[numpy.arange(int(k1),int(length))]*han2 #apply decay

    return y

def apply_delay(x, delay_s, srate):
    odd_flag = 0
    n = numpy.size(x)
    if n/2 == 1:     # ensure that there are an even number of points
        x[n] = numpy.empty()
        n = n-1
        odd_flag = 1   # will add a point at the end so the two will be same length

    n2 = n/2     # half of n

    # make a frequency vector
    fr = numpy.array([numpy.arange(1,int(n2))])
    freq = (numpy.transpose(fr) / (n2)) * (srate/2)
    pe = numpy.size(freq)
    print(pe)

    # get required phase shift vector
    phase_shift = -2*numpy.pi*freq[numpy.arange(1,int(n2)-1)]*delay_s  # skip highest freq comp.

    # apply fft
    xfft = numpy.fft.fft(x)

    # shift the positive frequencies
    xfft[numpy.arange(2,int(n2))] = xfft[numpy.arange(2,int(n2))] * numpy.exp(1j*phase_shift)

    # shift the negative frequencies
    xfft[n2+2:] = xfft[n2+2:] * numpy.exp(-1j*phase_shift[ ::-1]) # a(end:-1:1,: -> a[ ::-1,:]

# get the delayed waveform
    x_delayed = numpy.fft.ifft(xfft)
    if odd_flag == 1:
        x_delayed = numpy.concatenate((x_delayed,x_delayed[-1]))    # tack on a point to make odd again

    return x_delayed

def create_iad_noise(delay_us, atten_dB):

    x = signal()  # get noise sample

    #r,c = numpy.shape(x)
   # if c > r:
       # print('Error in CREATE_ITD_SIG! SIGNAL must be a COLUMN!')
        #return

    # apply rise-decay time:
    rpts = numpy.round(rise * srate)    # points in r/d
    x = hanwin(x,rpts)

    if numpy.abs(delay_us) > 0:
        sig_delayed = apply_delay(x, delay_us/1000000, srate)  # convert to sec.
        npts_silence = numpy.round(numpy.abs(delay_us/1000000) * srate)
        silence = numpy.zeros((npts_silence,1))
    else:
        sig_delayed = x
        npts_silence = 0
        silence = numpy.zeros(1)
    

    fact = 10**((atten_dB/2)/20)   # fact = 1 for atten_dB = 0

    pt_break = numpy.mod(npts_silence, numpy.size(signal)) # Find where the delayed signal is broken

    Binaural_Signal=numpy.zeros((2,(numpy.size(silence)+numpy.size(signal))))
    
    if delay_us >= 0:
        Binaural_Signal[:,1] = numpy.array([[x*fact], [silence]])
        Binaural_Signal[:,2] = numpy.array([[silence],[sig_delayed[pt_break+1:]/fact], [sig_delayed[1,pt_break]/fact]])
    else:
        Binaural_Signal[:,1] = numpy.array([[silence], [x*fact]]) # not sure if this is correct
        Binaural_Signal[:,2] = numpy.array([[sig_delayed[numpy.size(sig_delayed)-pt_break+1:]/fact], [sig_delayed[1,numpy.size(sig_delayed)-pt_break]/fact], [silence]])

    return create_iad_signal

