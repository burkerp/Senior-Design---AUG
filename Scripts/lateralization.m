% Program lateralization.m
% Written by Dan Ashmead, 8 Jan 2016
% Note: itd means interaural time difference, in microseconds
%       ild means interaural level difference, in decibels
% This program assumes that the following functions are in the Matlab path.
% Eventually these functions could be brought into this program as private
% functions, or even incorporated directly into the program code. Thanks to
% Wes Grantham for writing these functions.
%   create_iad_noise.m
%   create_noise.m
%   apply_delay.m
%   hanwin.m
%   ms1.m

clear;                 % Clear the Matlab memory work space

global StimulusSTR
StimulusSTR.SRATE = 44100;   % sample rate for sounds
StimulusSTR.Duration = 0.3;  % in seconds
StimulusSTR.Rise = .01;      % in seconds
StimulusSTR.HiPass = 100;    % high pass filter value in Hz
StimulusSTR.LoPass = 5000;   % low pass filter value in Hz
StimulusSTR.FilterOrder = 8; % filter order

reversal_limit = 12;   % Criterion number of reversals to run
down_rule = 3;         % Number of consecutive correct trials needed to decreasein stimulus level
reversal = 0;          % Initialize number of reversals to zero
consec_correct = 0;    % Initialize number of consecutive correct trials to zero
                       % We'll need to tweak these step sizes a bit:
stepsizes_itd = [50 10 5];  % Step sizes for changing itd value
stepsizes_ild = [1.5 .75 .25];   % Step sizes for changing ild value
itd_limits = [2 800];  % min and max allowable itd values
ild_limits = [0.1 8]   % min and max allowable ild values
stimulus_change = 1;   % Set "step size" or amount by which to change stimulus level
up = 1;                % Use the terms up and down to make it easier to read program
down = -1;
left = 1;              % Arbitrary designations for left and right
right = -1;
direction = 0;         % This keeps track of direction in which stimulus is changing
                       % It's set to zero ("neither"), then goes to up, down etc.                     
trial = 0;             % Initialize trial counter to zero
feedback = true;       % Whether to give feedback on whether vote is correct
pause_time = 0.5;      % Pause time between sound intervals, in seconds

% General instructions
display('Be sure you have stereo earphones, with left and right sides over the correct ears.');
display('Use your computer sound level control to set a comfortable level.');
display('On each trial you will hear two sounds, at different locations.');
display('Your task is to decide whether the second second was to the left or right of the first sound.')
display('After you vote, you will get feedback about whether you were correct on that trial.');
display('Please keep going until you see a Finished message.');

% Get user choice of which interaural cue to use, then set cue values
cue_type = input('Enter interaural cue to use, 1 for time difference, 2 for level difference: ','s');
cue_type = str2num(cue_type);
switch cue_type
    case 1
        itd = 125;  % Initial interaural time difference, will vary across trials
        ild = 0;    % Interaural level difference, stays the same across trials
    case 2
        itd = 0;    % Interaural level difference, stays the same across trials
        ild = 4;    % Initial interaural level difference, will vary across trials
end;
    

% Main program loop: Repeat this until criterion number of reversals is met
while reversal < reversal_limit
    
    trial = trial + 1; % Increase trial number
    
    stimulus_record(trial,1:2) = [itd ild];  % Keep track of stimulus levels
    
    % Display current stimulus level and number of reversals
    fprintf('Trial: %d  ITD: %5.1f  ILD:%5.1f  Reversals: %d\n',trial,itd,ild,reversal)
    
    % Get a random direction in which sound moves
    direction = sign(randn);  % direction is 1 for leftward or -1 for rightward
    
    % Build the binaural signal for the first and second sound intervals
    signal1 = create_iad_noise( direction .* itd ./ 2, direction .* ild ./ 2);
    sound1 = audioplayer(signal1,StimulusSTR.SRATE);
    % Build the binaural signal for the second sound interval
    signal2 = create_iad_noise( -direction .* itd ./ 2, -direction .* ild ./ 2);
    sound2 = audioplayer(signal2,StimulusSTR.SRATE);
    
    % Play the first sound
    playblocking(sound1);
    % Delay between sound intervals
    pause(pause_time);
     % Play the second sound
    playblocking(sound2);
    
    % Clear some variables from memory ... might not be necessary, but
    % Matlab is not so great with respect to memory management and these
    % are large-ish structures
    clear('signal1','signal2','sound1','sound2');
    
    % Loop to get vote ... subject is to press the F key if they think the
    % sound moved leftward, or the J key for rightward. Eventually we
    % should add some code so the subject doesn't have to press Enter, and
    % to keep prompting for entry until they press either F or J (that is,
    % in case they press another key besides F or J).
    vote_ok = false;
    while vote_ok == false
        vote = input('Press F key for left, J key for right, then press Enter','s');
        vote = upper(vote(1)); 
        if vote == 'F' | vote == 'J'
            vote_ok = true;
        end
    end
    
    % Classify vote as correct or incorrect, and optionally give feedback
    if (vote == 'F' & direction == -1) | (vote == 'J' & direction == 1)
        outcome = 'c';   % Correct vote
        if feedback
            display('Correct');
        end
    else
        outcome = 'i';   % Incorrect vote
        if feedback
            display('Wrong');
        end
    end
    
    % What to do, based on trial outcome of correct or incorrect
    if outcome == 'c'  % If trial outcome is correct
        consec_correct = consec_correct + 1;  % Increase count of corrects
        
        % Do the following if criterion # of consecutive corrects is met,
        % such that the stimulus level should be decreased to make the task
        % more difficult
        if consec_correct == down_rule
            consec_correct = 0;   % Reset # correct to zero
            if direction == up    % Possibly note a reversal
                reversal = reversal + 1;
            end;
            direction = down;     % Note that stimulus change direction is down
            
            % Set an index for which step size to use in changing stimulus
            % values. This is based on the current number of reversals.
            switch reversal
                case {0,1,2,3,4}
                    step_level = 1;
                case {5,6,7,8}
                    step_level = 2;
                otherwise
                    step_level = 3;
            end
            
            % Decrease the itd or ild
            switch cue_type
                case 1  % decrease itd, but not below the minimum allowable value
                    itd = itd - stepsizes_itd(step_level);
                    if itd < itd_limits(1)
                        itd = itd_limits(1);
                    end
                case 2  % decrease ild, but not below the minimum allowable value
                    ild = ild - stepsizes_ild(step_level);
                    if ild < ild_limits(1)
                        ild = ild_limits(1);
                    end
            end
            
        end;
        
    else    % If trial outcome is incorrect
        consec_correct = 0;   % Note that # correct is zero
        if direction == down  % Possibly note a reversal
            reversal = reversal + 1;
        end;
        direction = up;   % Note that stimulus change direction is up
        
        % Set an index for which step size to use in changing stimulus
        % values. This is based on the current number of reversals.
        switch reversal
            case {0,1,2,3,4}
                step_level = 1;
            case {5,6,7,8}
                step_level = 2;
            otherwise
                step_level = 3;
        end
        
        % Increase the itd or ild
        switch cue_type
            case 1  % increase itd, but not above the maximum allowable value
                itd = itd + stepsizes_itd(step_level);
                if itd > itd_limits(2)
                    itd = itd_limits(2);
                end
            case 2  % increase ild, but not above the maximum allowable value
                ild = ild + stepsizes_ild(step_level);
                if ild > ild_limits(2)
                    ild = ild_limits(2);
                end
        end
        
    end;
    
end;

% Save the data.
% Not implemented yet ... eventually we will save the matrix
% stimulus_record and use it to calculate a threshold, based on the final,
% say, 6 or 8 reversal points. 
% For now, plot the stimulus_record. The rows correspond to trial numbers.
% The first column is the ITD value, second column is the ILD value on that
% trial. Depending on whether ITD or ILD was selected as the stimulus
% dimension to focus on, that one will change across trials, and the other
% one will be zero across all trials.
plot(stimulus_record,'-o')
xlabel('Trial number')
ylabel('Interaural time (us) or level (dB) difference')

display('Finished with this measurement.');