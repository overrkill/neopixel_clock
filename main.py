import machine, time
from neopixel import NeoPixel
import ntptime

# At the top of the file
IST_OFFSET   = 19800
NUM_PIXELS   = 92
COLOR_ON     = (10, 10, 0)
COLOR_OFF    = (0, 0, 0)
DATA_PIN     = 2
POLL_INTERVAL = 1000
NTP_INTERVAL = 900000
SEGMENTS = (
    (1,1,0,0,0,0,0),#1
    (0,1,1,0,1,1,1),#2
    (1,1,1,0,0,1,1),#3
    (1,1,0,1,0,0,1),#4
    (1,0,1,1,0,1,1),#5
    (1,0,1,1,1,1,1),#6
    (1,1,1,0,0,0,1),#7
    (1,1,1,1,1,1,1),#8
    (1,1,1,1,0,0,1),#9
    (1,1,1,1,1,1,0)#0
)
def getNumber(no):
    return SEGMENTS[no] if 0 <= no <= 9 else (0,0,0,0,0,0,0)
    # if no == 1 :return [1,1,0,0,0,0,0]
    # elif no == 2 :return [0,1,1,0,1,1,1]
    # elif no == 3 :return [1,1,1,0,0,1,1]
    # elif no == 4 :return [1,1,0,1,0,0,1]
    # elif no == 5 :return [1,0,1,1,0,1,1]
    # elif no == 6 :return [1,0,1,1,1,1,1]
    # elif no == 7 :return [1,1,1,0,0,0,1]
    # elif no == 8 :return [1,1,1,1,1,1,1]
    # elif no == 9 :return [1,1,1,1,0,0,1]
    # elif no == 0 :return [1,1,1,1,1,1,0]
    # else :return [0,0,0,0,0,0,0]
    
def setNtpTime():
    ntptime.settime()

def drawSeg(idx,i,np,color):
    start = (idx*28)+(4*i)
    np[start]=color
    np[start+1]=color
    np[start+2]=color
    np[start+3]=color

def drawDigit(curr, prev ,index,np):
    currSegs= getNumber(curr)
    prevSegs= getNumber(prev)
    
    for i in range(0,7):
        if(currSegs[i]==prevSegs[i]):#draw segment
            pass
        elif currSegs[i]==1:
            drawSegbySeg(index*7+i,np,(10,10,0))
        else:
            drawSegbySeg(index*7+i,np,(0,0,0))#disable the segment
        

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

def ledTest(np):
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

led = machine.Pin(DATA_PIN, machine.Pin.OUT)  # GPIO2 = onboard LED
np = NeoPixel(led,NUM_PIXELS)
# setNtpTime()
prev = [None, None ,None , None]

ntptime.settime()
lastNtp = time.ticks_ms()
lastPoll = time.ticks_ms()


np.fill((0,0,0))
np.write()
# animation_box(np)
# for i in range(0,23):
#     np.fill((0,0,0))
#     drawSegbySeg(i,np,(10,20,0))
#     np.write()
#     time.sleep(0.1)
# for i in range(0,10):
#     drawDigit(i,i-1,2,np)
#     time.sleep(0.5)
while True:
    now = time.ticks_ms()
    epo = time.time()
    # global prev
    tm = time.localtime(epo+IST_OFFSET)
    hh = tm[3]%12
            # hour[0], hour[1], minute[0], minute[1]
    digits = [hh//10, hh%10,   m[4]//10,    tm[4]%10]
    if time.ticks_diff(now, lastNtp) >= NTP_INTERVAL:
        try:
            ntptime.settime()
        except:
            pass
        lastNtp = now
    
    if time.ticks_diff(now, lastPoll) >=POLL_INTERVAL:
        for i in range(0,4):
            if digits[i] != prev[i]:
                if i == 0:
                    if digits[i] == 1:
                        drawSegbySeg(21,np ,COLOR_ON)
                        drawSegbySeg(22,np ,COLOR_ON)
                    else :
                        drawSegbySeg(21,np ,COLOR_OFF)
                        drawSegbySeg(21,np ,COLOR_OFF)
                else:
                    drawDigit(digits[i],prev[i],3-i,np)
                prev[i] = digits[i]
        np.write()
        lastPoll = now
    # if (digits[0]!=prev[0] or digits[1]!=prev[1] or digits[2]!=prev[2] or digits[3]!=prev[3]) :
    #     # prev=digits
    #     # drawNumber(0,digits[3],np)
    #     drawDigit(digits[3],prev[3],0,np)
    #     drawDigit(digits[2],prev[2],1,np)
    #     drawDigit(digits[1],prev[1],2,np)
    #     # drawNumber(1,digits[2],np)
    #     # drawNumber(2,digits[1],np)
    #     # drawNumber(3,h1,np)
    #     if(digits[0]==1 and prev[0] == 0):
    #         drawSeg(3,0,np,(5,5,0))
    #         drawSeg(3,1,np,(5,5,0))
    #     elif (digits[0]== 0 and prev[0] == 1) : 
    #         drawSeg(3,0,np,(0,0,0))
    #         drawSeg(3,1,np,(0,0,0))
    #     else:
    #         pass
    #     prev=digits
    # time.sleep(10)
