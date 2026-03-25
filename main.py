import machine, time
from neopixel import NeoPixel
import ntptime

# At the top of the file
IST_OFFSET   = 19800
NUM_PIXELS   = 92
COLOR_ON     = (10, 10, 0)
COLOR_OFF    = (0, 0, 0)
DAY_YELLOW   = (20,10,0)
DAY_BLUE     = (0,10,20) 
DATA_PIN     = 2
POLL_INTERVAL = 1000
DATE_POLL    = 30000
NTP_INTERVAL = 900000
SEGMENTS = {
    1:(1,1,0,0,0,0,0),#1
    2:(0,1,1,0,1,1,1),#2
    3:(1,1,1,0,0,1,1),#3
    4:(1,1,0,1,0,0,1),#4
    5:(1,0,1,1,0,1,1),#5
    6:(1,0,1,1,1,1,1),#6
    7:(1,1,1,0,0,0,1),#7
    8:(1,1,1,1,1,1,1),#8
    9:(1,1,1,1,0,0,1),#9
    0:(1,1,1,1,1,1,0)#0
    }

def getNumber(no):
    return SEGMENTS.get(no, (0,0,0,0,0,0,0))

def drawSeg(idx,i,np,color):
    start = (idx*28)+(4*i)
    np[start]=color
    np[start+1]=color
    np[start+2]=color
    np[start+3]=color

def drawDigit(curr, prev ,index,np,color=COLOR_ON,force=False):
    currSegs= getNumber(curr)
    prevSegs= getNumber(prev)
    
    for i in range(0,7):
        if(currSegs[i]==prevSegs[i] and not force ):#draw segment
            pass
        elif currSegs[i]==1:
            drawSegbySeg(index*7+i,np,color)
        else:
            drawSegbySeg(index*7+i,np,COLOR_OFF)#disable the segment


def drawSegbySeg(segNum,np,color):
    start = segNum*4
    np[start]=color
    np[start+1]=color
    np[start+2]=color
    np[start+3]=color

def drawNumber(idx, num,np):
    seg = getNumber(num)
    for i in range(0,7):
        if seg[i]==1:
            drawSeg(idx,i,np,(10,5,0))

def ledTestAnimation(np):
    for i in range(0,93):
        np[i] = (int(0.8*i),int(0.4*i),int(0.2*i))
        np.write()
        time.sleep(0.5)


def animation_box(np):
    segs = [0,1,2,9,16,17,18,19,12,5]
    for i in segs:
        np[i*4] = (int(5*i),40,40)
        np.write()
        time.sleep(0.2)
        np[i*4+1] = (5*i,40,40)
        np.write()
        time.sleep(0.2)
        np[i*4+2] = (5*i,40,40)
        np.write()
        time.sleep(0.2)
        np[i*4+3] = (5*i,40,40)
        np.write()
        time.sleep(0.2)
    np.fill((0,0,0))

def animationBoxbySeg(np):
    for i in range(0,23):
        np.fill((0,0,0))
        drawSegbySeg(i,np,(10,20,0))
        np.write()
        time.sleep(0.3)

def digitCountdown(np):
    for i in range(0,10):
        drawDigit(i,i-1,2,np,(20,10,0))
        drawDigit(i,i-1,1,np,(0,10,20))
        drawDigit(i,i-1,0,np,(10,30,10))
        np.write()
        time.sleep(0.5)
    np.fill(COLOR_OFF)

led = machine.Pin(DATA_PIN, machine.Pin.OUT)  # GPIO2 = onboard LED
np = NeoPixel(led,NUM_PIXELS)
prev = [None, None ,None , None]

ntptime.settime()
lastNtp = time.ticks_ms()
lastPoll = time.ticks_ms()
lastDatePoll = time.ticks_ms()

np.fill((0,0,0))
np.write()
lastSec = False
lastDateShown=False
digitCountdown(np)

while True:
    now = time.ticks_ms()
    epo = time.time()
    # global prev
    tm = time.localtime(epo+IST_OFFSET)
    hh =   tm[3]%12 if tm[3]>12 else tm[3]
            # hour[0], hour[1], minute[0], minute[1]
    digits = [hh//10, hh%10,   tm[4]//10,    tm[4]%10]
    date = [tm[1]//10,tm[1]%10,tm[2]//10,tm[2]%10]

    ## after every 15 mins recalibrate
    if time.ticks_diff(now, lastNtp) >= NTP_INTERVAL:
        try:
            ntptime.settime()
        except:
            pass
        lastNtp = now

    # set color based on day or night 
    currentColor1 = DAY_YELLOW if 8 <= tm[3] <=22 else COLOR_ON
    currentColor2 = DAY_BLUE if 8 <= tm[3] <=22 else COLOR_ON

#if date polling distance has elapsed
    if time.ticks_diff(now, lastDatePoll) >=DATE_POLL:
        for i in range(0,4):
            if date[i] != prev[i]:
                if i == 0:
                    if date[i] == 1:
                        drawSegbySeg(21,np ,currentColor1)
                        drawSegbySeg(22,np ,currentColor1)
                    else :
                        drawSegbySeg(21,np ,COLOR_OFF)
                        drawSegbySeg(22,np ,COLOR_OFF)
                else:
                    drawDigit(date[i],prev[i],3-i,np,currentColor1,not lastDateShown)
                prev[i] = date[i]
        lastDatePoll = now
        lastDateShown = True
        np.write()
    elif time.ticks_diff(now, lastPoll) >=POLL_INTERVAL and time.ticks_diff(now,lastDatePoll) >= 10000:
        for i in range(0,4):
            if digits[i] != prev[i]:
                if i == 0:
                    if digits[i] == 1:
                        drawSegbySeg(21,np ,currentColor1)
                        drawSegbySeg(22,np ,currentColor1)
                    else :
                        drawSegbySeg(21,np ,COLOR_OFF)
                        drawSegbySeg(22,np ,COLOR_OFF)
                else:
                    drawDigit(digits[i],prev[i],3-i,np,currentColor2 if i > 1 else currentColor1,lastDateShown)
                prev[i] = digits[i]
        if lastSec:
            np[48]=(20,0,0)
        else :
            np[48]=COLOR_OFF
        lastDateShown = False
        lastSec= not lastSec
        np.write()
        lastPoll = now
