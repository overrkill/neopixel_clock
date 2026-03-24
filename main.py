import machine, time
from neopixel import NeoPixel
import ntptime

def getNumber(no):
    if no == 1 :return [1,1,0,0,0,0,0]
    if no == 2 :return [0,1,1,0,1,1,1]
    if no == 3 :return [1,1,1,0,0,1,1]
    if no == 4 :return [1,1,0,1,0,0,1]
    if no == 5 :return [1,0,1,1,0,1,1]
    if no == 6 :return [1,0,1,1,1,1,1]
    if no == 7 :return [1,1,1,0,0,0,1]
    if no == 8 :return [1,1,1,1,1,1,1]
    if no == 9 :return [1,1,1,1,0,0,1]
    if no == 0 :return [1,1,1,1,1,1,0]
    
def setNtpTime():
    ntptime.settime()

def drawSeg(idx,i,np,color):
    start = (idx*28)+(4*i)
    np[start]=color
    np[start+1]=color
    np[start+2]=color
    np[start+3]=color

def drawNumber(idx, num,np):
    seg = getNumber(num)
    for i in range(0,7):
        if seg[i]==1 :
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


led = machine.Pin(2, machine.Pin.OUT)  # GPIO2 = onboard LED
np = NeoPixel(led,92)
# setNtpTime()


ntptime.settime()
np.fill((0,0,0))
animation_box(np)
prevhh = 0 
prevmm = 0 
while True:
    # animation_box(np)
    # ledTest(np)
    # np[0] = (0,0,0)
    # time.sleep(0.5)
    # np[0] = (10,10,10)
    # np.write()
    # time.sleep(0.5)
    # np[0] = (0,0,0)
    # np.write()

    # np.write()
    # time.sleep(0.5)
    # time.sleep(10)
    tm = time.localtime()
    if prevhh != tm[3] or prevmm != tm[4] :
        prevhh = tm[3] 
        prevmm = tm[4]
        mm = tm[4]
        inc = 0
        if(mm > 30):
            mm = mm%30
            inc = 1 
        else:
            mm = mm+30
        m2 = mm%10 # minute units place 
        m1 = mm//10 # minute tens 
        hh = (tm[3]+5+inc)%12
        if hh == 0 :
            hh = 12
        h2 = hh%10
        h1 = hh//10
        np.fill((0,0,0))
        np.write()
        drawNumber(0,m2,np)
        drawNumber(1,m1,np)
        drawNumber(2,h2,np)
    # drawNumber(3,h1,np)
        if(h1==1):
            drawSeg(3,0,np,(5,5,0))
            drawSeg(3,1,np,(5,5,0))
        np.write()
    time.sleep(10)
