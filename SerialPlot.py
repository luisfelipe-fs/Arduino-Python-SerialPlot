from __future__ import print_function

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

timeList = deque(maxlen=5000)
audioList = deque(maxlen=5000)
stopThread = False

# Porta COM1, COM2, etc. no windows
s = serial.Serial('/dev/ttyACM1', baudrate=31250)

# Removendo lixo
for i in range(25): line = s.readline()

def setDuration (seconds):
    return int(seconds/0.02)

def getSerialData ():
    global s, stopThread

    count = 0
    maxCount = setDuration(10)
    while not stopThread and count < maxCount:
        try:
            line = s.readline()
        except UnicodeDecodeError:
            print("Encontrou algum lixo: ", line)
            continue

        try:
            readt, readA = [int(x) for x in line.decode('utf-8')[:-2].split()]
        except ValueError:
            print("Encontrou algum lixo: ", line)
            continue
        
        timeList.append(readt/1000.)
        audioList.append(readA/1023.*5)
        count += 1

thread = threading.Thread(target=getSerialData)
thread.start()

def onlinePlot (i, timeList, tempList):
    ax.clear()
    ax.set_title("Afinador")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Amplitude")
    ax.plot(timeList, tempList)

print('Conectado a porta %s.\n\n' % s.name)

fig = plt.figure()
ax = plt.axes()

ani = animation.FuncAnimation(fig, onlinePlot, fargs=(timeList, audioList), interval=1)
try:
    plt.show()
except AttributeError:
    stopThread = True
    print("Fechou o plot.")
    s.close()
    
print("Salvando em arquivo...")
with open(".data/Dados.txt", "w") as f:
    f.writelines(["%s %s\n" % (t, a) for t, a in zip(timeList, audioList)])
print("Feito.")
