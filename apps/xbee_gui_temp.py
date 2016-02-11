import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from socket import *
from struct import *


plt.close('all')
sock = socket(AF_INET, SOCK_DGRAM)
sock.sendto("hello", ("127.0.0.1", 10001))
start_time = time.time()

fig, ax = plt.subplots()

tam=30
ydata1 = [0] * tam		#cantidad		
ydata2 = [0] * tam		#cantidad	
ax1=plt.axes()  
ax1.legend()
# make plot
line1, = plt.plot(ydata1,'ro-',label='XbeeS2')
line2, = plt.plot(ydata2,'bo-',label='XbeePro')
plt.ylim([-5,35]) 
plt.grid(True)
plt.xlabel('Tiempo[s]')
plt.ylabel('Temperatura [C]')
plt.legend()


def animate(i):
	data = sock.recv(200)			#data = [0x01,0x32,0x34,',',0x30]
	cur_time = time.time()-start_time

	if ord(data[0])==0x01:
		valor1 = 10*(ord(data[1])-0x30) +(ord(data[2])-0x30) +0.1*(ord(data[4])-0x30)
		valor2 = 0
	elif ord(data[0])==0x02:
		valor1 = 0
		valor2 = 10*(ord(data[1])-0x30) +(ord(data[2])-0x30) +0.1*(ord(data[4])-0x30)
	else:
		print "Paquete erroneo",data
		valor2 =0
		valor1 = 0
	
	print "t:",cur_time,"s","XbeeS2 T=",valor1,"C", "/ XbeePRO T=",valor2,"C" 
	
	plt.xlim([cur_time-len(ydata1),cur_time])	
	ydata1.append(valor1)			#actializa valor lista agrega nuevo valor
	del ydata1[0]	
	line1.set_xdata(np.linspace(cur_time-len(ydata1),cur_time,len(ydata1)))
	line1.set_ydata(ydata1)  		# update the data
	
	ydata2.append(valor2)			#actializa valor lista agrega nuevo valor
	del ydata2[0]	
	line2.set_xdata(np.linspace(cur_time-len(ydata2),cur_time,len(ydata2)))
	line2.set_ydata(ydata2)  		# update the data	


ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
