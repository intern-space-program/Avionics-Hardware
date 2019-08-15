from udp_server import udp_network
import time
from datetime import datetime

server = udp_network('127.0.0.1',5005)

#Make a Sample Packet:
packet_num = 1
altitude = 10000.0123
#time_rn = datetime.now().strftime('%Y -%m-%d %H:%M:%S')
longitude = 101
latitude = 102
gyrox = 103
gyroy = 104
gyroz = 105
aclx = 106
acly = 107
aclz = 108

names = ['packet_num','altitude','longitude','latitude','gyrox','gyroy','gyroz','aclx','acly','aclz']
data = [packet_num,altitude,longitude,latitude,gyrox,gyroy,gyroz,aclx,acly,aclz]
#server.recieve_encoded_datagram(data,names)
server.recieve_datagram()
