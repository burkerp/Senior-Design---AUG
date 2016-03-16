def create_iad_noise(delay_us, atten_dB):
    # function Binaural_Signal = create_iad_noise(delay_us, atten_dB)
    # Modified (simplified) from Gifford function create_iad_sig.m.
    # Creates a binaural signal with the specified ITD and ILD.
    # Positive values produce image toward the left ear (channel 1) -
    #  i.e., left ear leading or more intense. Negative values produce
    #  image toward the right ear (channel 2).
    # Zeros are inserted/appended as needed at the onset/offset of the appropriate
    # channels for the delayed signal. Thus, the length of the columns will be longer
    # than that of the individual signals by an amount depending
    # on the delay.
    # Makes use of the function APPLY_DELAY.

    global StimulusSTR

    # set parameters ... commented out because these are set in calling program
    # StimulusSTR.SRATE = 44100;
    # StimulusSTR.Duration = 0.3;  % in seconds
    # StimulusSTR.Rise = .01;      % in seconds
    # StimulusSTR.HiPass = 100;
    # StimulusSTR.LoPass = 5000;
    # StimulusSTR.FilterOrder = 4;

    signal = create_noise  # get noise sample
    srate = StimulusSTR.SRATE

    [r,c] = size(signal)
    if c > r:
        disp('Error in CREATE_ITD_SIG! SIGNAL must be a COLUMN!')
        return
    end

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
    end

    fact = 10.^((atten_dB/2)/20)   # fact = 1 for atten_dB = 0

    pt_break = mod(npts_silence, length(signal)) # Find where the delayed signal is broken

    if delay_us >= 0:
        Binaural_Signal[:,1] = array([signal*fact], [silence])
        Binaural_Signal[:,2] = [ [silence], [sig_delayed(pt_break+1,end)/fact], [sig_delayed(1,pt_break)/fact]]
    else:
        Binaural_Signal[:,1] = array([silence], [signal*fact]) # not sure if this is correct
        Binaural_Signal[:,2] = [ [sig_delayed(end-pt_break+1,end)/fact], [sig_delayed(1,end-pt_break)/fact], [silence] ]
    end

    return Binaural_Signal