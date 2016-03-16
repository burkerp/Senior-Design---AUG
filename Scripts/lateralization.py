import numpy
import pyaudio
import random
import time

stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=1,rate=44100,output=True)

srate=44100
duration=0.3
rise=0.01
hipass=100
lopass=5000
filterorder=8

reversal_limit=12
down_rule=3
reversal=0
consec_correct=0

stepsizes_itd=numpy.array([50, 10, 5])
itd_limits=numpy.array([2, 800])
stimulus_change=1
up=1
down=-1
left=1
right=-1
direction=0
trial=0
feedback=1
pause_time=0.5

itd=125
ild=0

while reversal<reversal_limit:
    trial=trial+1
    stimulus_record=numpy.array([itd, ild])
    direction=numpy.sign(numpy.random.randint(-5,5))

    signal1 = create_iad_noise( direction * itd / 2, direction * ild / 2)
    sound1 = audioplayer(signal1,srate)
     
    signal2 = create_iad_noise( -direction * itd / 2, -direction * ild / 2)
    sound2 = audioplayer(signal2,srate)

    for n in range(0,22000,1): stream.write(chr(int(random.random()*256)))
    time.sleep(1.2)
    for n in range(0,22000,1): stream.write(chr(int(random.random()*256)))

    stream.close()
    pyaudio.PyAudio().terminate()

    vote_ok=0

    while vote_ok==0:
        vote=input("Press F key for left, J key for right, then press Enter.")
        vote=vote.upper()
        if vote=='F' or vote=='J':
            vote_ok=1
    if (vote == 'F' and direction == -1) or (vote == 'J' and direction == 1):
        outcome = 'c'   
        if feedback:
            print('Correct')
    else:
        outcome= 'i'
        if feedback:
            print('Wrong')
    if outcome == 'c': 
        consec_correct = consec_correct + 1        
        if consec_correct == down_rule:
            consec_correct = 0   
            if direction == up:   
                reversal = reversal + 1
        direction = down
        if reversal==0 or 1 or 2 or 3 or 4:
            step_level=1
        if reversal==5 or 6 or 7 or 8:
            step_level=2
        else:
            step_level=3
        itd = itd - stepsizes_itd[step_level]
        if itd < itd_limits[1]:
            itd = itd_limits[1]
    else:
        consec_correct = 0
        if direction == down:
            reversal = reversal + 1
        direction = up 
        if reversal==0 or 1 or 2 or 3 or 4:
            step_level=1
        if reversal==5 or 6 or 7 or 8:
            step_level=2
        else:
            step_level=3
        itd = itd + stepsizes_itd[step_level]
        if itd > itd_limits[2]:
            itd = itd_limits[2]            

  
