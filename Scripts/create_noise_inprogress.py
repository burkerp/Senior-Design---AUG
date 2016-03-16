def create_noise():  # get noise sample
    srate = StimulusSTR.SRATE

    [r,c] = size(signal)
    if c > r:
        disp('Error in CREATE_ITD_SIG! SIGNAL must be a COLUMN!')
        return


    # apply rise-decay time:
    rpts = round(StimulusSTR.Rise * srate)    # points in r/d
    signal = hanwin(signal,rpts)

    if numpy.abs(delay_us) > 0:
        sig_delayed = apply_delay(signal, delay_us/1E6, srate)  # convert to sec.
        npts_silence = round(abs(delay_us/1E6) * srate)
        silence = zeros(npts_silence,1)
    else:
        sig_delayed = signal
        npts_silence = 0
        silence = []


    fact = 10**((atten_dB/2)/20)   # fact = 1 for atten_dB = 0

    pt_break = mod(npts_silence, length(signal)) # Find where the delayed signal is broken

    if delay_us >= 0:
        Binaural_Signal[:,1] = [signal*fact, silence]
        Binaural_Signal[:,2] = [silence, sig_delayed(pt_break+1,end)/fact, sig_delayed(1,pt_break)/fact]
    else:
        Binaural_Signal[:,1] = [silence, signal*fact]
        Binaural_Signal[:,2] = [sig_delayed(end-pt_break+1,end)/fact, sig_delayed(1,end-pt_break)/fact, silence]


    return Binaural_Signal