from udp_server import udp_network

server = udp_network('192.168.43.166',5005)

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