import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

timeList = deque(maxlen=1000)
tempList = deque(maxlen=1000)

s = serial.Serial('/dev/ttyACM0') # COLOCA A PORTA DO TEU ARDUINO AQUI
for i in range(20): s.readline()

def getSerialData ():
    while True:
        global s
        try:
            line = s.readline()
        except:
            return
        try:
            readt, readA = [int(x) for x in str(line, 'utf-8')[:-2].split()]
            timeList.append(readt)
            audioList.append(readA/1023.*5)
        except:
            pass

thread = threading.Thread(target=getSerialData)
thread.start()

def onlinePlot (i, timeList, tempList):
    ax.clear()
    ax.set_title("Amplitude Monitor")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Amplitude (dB)")
    ax.plot(timeList, tempList)

print('Conected to %s.' % s.name)

fig = plt.figure()
ax = plt.axes()

ani = animation.FuncAnimation(fig, onlinePlot, fargs=(timeList, audioList), interval=1)
plt.show()

s.close()
