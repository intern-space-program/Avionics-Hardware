import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from udp_server2 import udp_network

def animate(i, udpserver,packnums,y1s,y2s,y3s,y4s,y5s,y6s):

    packetnum, acceleration, altitude, longitude, latitude, temperature, orientation, pressure = ("",)*8
    newdata = [packetnum, acceleration, altitude, longitude, latitude, temperature, orientation, pressure]
    names = ['packetnum', 'acceleration', 'altitude', 'longitude', 'latitude', 'temperature', 'orientation', 'pressure']
    udpserver.recieve_simple_encoded_datagram(newdata,names)

    newdata = udpserver.decoded_datagram

    #print("mynewdata")
    #print(newdata)
    packetnum, acceleration, altitude, longitude, latitude, temperature, orientation, pressure = newdata

    prev_packnum = -1
    if(int(packetnum)>prev_packnum):
        packnums.append(int(packetnum))
        y1s.append(float(temperature))
        y2s.append(float(altitude))
        y5s.append(float(pressure))
        #y6s.append(float(pressure))
        if latitude != "None":
            y3s.append(float(latitude))
            y4s.append(float(longitude))
        prev_packnum = int(packetnum)
    # try:
    #     if(int(packetnum)>prev_packnum):
    #         packnums.append(int(packetnum))
    #         ys.append(float(temperature))
    #         prev_packnum = int(packetnum)
    # except:
    #     pass
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    ax1.plot(packnums,y1s,'r')
    ax1.set_ylabel('Temperature [c]')
    ax1.set_xlabel('Packet num')
    ax1.set_title("Temperature vs packet num")
    ax1.set_xlim(left=max(0,packnums[i]-50),right=packnums[i])
    ax1.grid()

    ax2.plot(packnums,y2s,'r')
    ax2.set_ylabel('Altitude [ft]')
    ax2.set_xlabel('Packet num')
    ax2.set_title("Altitude vs packet num")
    ax2.set_xlim(left=max(0,packnums[i]-50),right=packnums[i])
    ax2.grid()

    ax3.plot(y4s,y3s,'r')
    ax3.set_ylabel('Latitude')
    ax3.set_xlabel('Longitude')
    ax3.set_title("Longitude vs Latitude")
    ax3.grid()

    ax4.plot(packnums,y5s,'r')
    ax4.set_xlabel('Packet num')
    ax4.set_ylabel('Pressure [psi]')
    ax4.set_title("Pressure vs packet num")
    ax4.set_xlim(left=max(0,packnums[i]-50),right=packnums[i])
    ax4.grid()
    plt.figtext(0.7, 0.7,"ALTITUDE:"+str(round(y2s[i],2))+"[ft]", bbox=dict(facecolor='red', alpha=0.5),wrap=True,fontsize=18)
    #plt.figtext(0.7, 0.6,"TEMPERATURE:"+str(round(y1s[-1],2))+"[C]", bbox=dict(facecolor='red', alpha=0.5),wrap=True,fontsize=18)
    #plt.figtext(0.7, 0.5,"PRESSURE:"+str(round(y5s[-1],2))+"[Psi]", bbox=dict(facecolor='red', alpha=0.5),wrap=True,fontsize=18)
    plt.tight_layout()
    
    
    
##########################

server = udp_network('127.0.0.1',5005)
server.bindConnection()

fig = plt.figure(figsize=(14,6))

plt.rcParams.update({'font.size': 15})
fig.set_facecolor('gray')
#plt.figtext(0.75,0.3 ,"Comment: Test string that is a note about something", wrap=True,horizontalalignment='center', fontsize=12)
ax1 = fig.add_subplot(2,3,1)
ax1.set_facecolor((0.83, 0.83,0.83))
ax2 = fig.add_subplot(2,3,2)
ax2.set_facecolor((0.83, 0.83,0.83))
ax3 = fig.add_subplot(2,3,4)
ax3.set_facecolor((0.83, 0.83,0.83))
ax4 = fig.add_subplot(2,3,5)
ax4.set_facecolor((0.83, 0.83,0.83))

packetAr = []
y1ar = []
y2ar = []
y3ar = []
y4ar = []
y5ar = []
y6ar = []

ani = animation.FuncAnimation(fig, animate, fargs=(server,packetAr,y1ar,y2ar,y3ar,y4ar,y5ar,y6ar,), interval=1)

plt.show()

