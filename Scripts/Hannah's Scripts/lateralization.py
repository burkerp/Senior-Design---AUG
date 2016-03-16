import numpy
import external
import pyaudio
import random
import time
import pylab as pl

#initialize variables

srate=44100    #sample rate
duration=0.3   #seconds
rise=0.01      #seconds
hipass=100     #high pass filter in Hz
lopass=5000    #low pass filter in Hz
filterorder=8  #filter order

reversal_limit=12 #number of reversals to run
down_rule=3       #number of consecutive correct trials to decrease stimulus difference
reversal=0        #initialize number of reversals to zero
consec_correct=0  #initialize number of consecutive correct trials to zero

stepsizes_itd=numpy.array([50, 10, 5])  #three decreasing step sizes for changing itd
itd_limits=numpy.array([2, 800])        #max and min itd
stimulus_change=1                       #initialize step size
up=1               #up, down, left, and right arbitrarily assigned
down=-1
left=1
right=-1
direction=0        #initialize change direction to zero
trial=0            #initialize trial number 
feedback=1         #whether give feedback on vote
pause_time=12000   #pause time between sounds

itd=125    #tests based on time difference, varies based on trial
ild=0      #level difference does not change

#main program loop: runs until max reversals limit

while reversal<reversal_limit:
    
    trial=trial+1            #increase trial number
    
    stimulus_record=numpy.array([itd, ild])     #records stimulus levels
    
    direction=numpy.sign(numpy.random.randint(-5,5))   #randomly assigns left if 1, right if -1

    stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=2,rate=srate,output=True)  #open PyAudio, initialize sampling rate

    #create binaural signal for first sound, relies on create_iad_noise
    signal1 = external.create_iad_noise( direction * itd / 2, direction * ild / 2)
    sound1 = chr(int(signal1))
    
    #create binaural signal for second sound 
    signal2 = external.create_iad_noise( -direction * itd / 2, -direction * ild / 2)
    sound2 = chr(int(signal2))
    

    stream.write(sound1)     #play first sound
    time.sleep(pause_time)   #pause
    stream.write(sound2)     #play second sound

    stream.close()
    pyaudio.PyAudio().terminate()    #close PyAudio

    vote_ok=0

#The next section needs to be altered to make it compatible with website.
    while vote_ok==0:
        vote=numpy.raw_input("Press F key for left, J key for right, then press Enter.")
        vote=vote.upper()    #capitalizes input
        if vote=='F' or vote=='J':    
            vote_ok=1        #continue through loop
            
    if (vote == 'F' and direction == -1) or (vote == 'J' and direction == 1):
        outcome = 'c'   
        if feedback:
            print('Correct')
    else:
        outcome= 'i'
        if feedback:
            print('Wrong')
            
    if outcome == 'c':    #correct answer
        consec_correct = consec_correct + 1     #update number of consecutive correct answers   

        if consec_correct == down_rule:    #if the number of correct answers is met
            consec_correct = 0          #reset after set criterion
            if direction == up:   
                reversal = reversal + 1    #update reversal number
        direction = down
        
        if 0<=reversal<=4:    #larger changes for the first reversals
            step_level=1
        if 5<=reversal<=8:    #changes become smaller for subsequent reversals  
            step_level=2
        else:
            step_level=3
            
        itd = itd - stepsizes_itd[step_level]    #itd decreases based on set stepsizes
        if itd < itd_limits[1]:
            itd = itd_limits[1]
            
    else:           #incorrect answer
        consec_correct = 0     #reset to zero
        if direction == down:
            reversal = reversal + 1     #update reversal number
        direction = up
        
        if 0<=reversal<=4:    #larger changes for the first reversals
            step_level=1
        if 5<=reversal<=8:    #changes become smaller for subsequent reversals  
            step_level=2
        else:
            step_level=3
            
        itd = itd + stepsizes_itd[step_level]      #itd increases based on set stepsizes
        if itd > itd_limits[2]:
            itd = itd_limits[2]            

pl.plot(stimulus_record)
pl.plot(stimulus_record, '*')
pl.xlabel('Trial number')
pl.ylabel('Interaural time difference (us)')
pl.show()
