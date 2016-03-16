function signal = create_noise
% function signal = create_noise
%  Jan 7, 2016
%  Modification (simplification) of Gifford function iad_rg_setup_signal.m
%  Creates a bandpass noise to be used for IAD experiment

global StimulusSTR

    npts = round(StimulusSTR.Duration * StimulusSTR.SRATE);
    signal = randn(npts,1);
    % filter it
    cutoffs = [StimulusSTR.HiPass StimulusSTR.LoPass]/(StimulusSTR.SRATE/2);
    [b, a] = butter(StimulusSTR.FilterOrder/2, cutoffs);  %take half of specified filter order, since we're using filtfilt.
    signal = filtfilt(b,a,signal);

signal = signal/rms1(signal);  % scale to an RMS of 1

