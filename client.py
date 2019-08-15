from udp_server import udp_network
import time
from datetime import datetime

server = udp_network('127.0.0.1',5005)

#Make a Sample Packet:
packetnum = ''
acceleration = ''
altitude = ''
longitude = ''
latitude = ''
temperature = ''
orientation = ''
pressure = ''

names = ['packetnum', 'acceleration', 'altitude', 'longitude', 'latitude', 'temperature', 'orientation', 'pressure']
data = [packetnum, acceleration, altitude, longitude, latitude, temperature, orientation, pressure]
server.recieve_simple_encoded_datagram(data,names)