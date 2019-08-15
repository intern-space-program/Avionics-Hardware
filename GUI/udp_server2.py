#Title: UDP Server with datagram encoding and decoding
#Author: Dillan McDonald + Connor Jakubik
#Version: 1.1
#Date: 07/22/19
# NOTE: removed infinite loops and prints
# You must always generate a format string before encoding or decoding

import socket
from struct import pack , unpack ,unpack_from

class udp_network:
    def __init__(self,server_ip,port):
        self.port = port
        self.ip = server_ip
        self.format_string = ''
        self.decoded_datagram = []
        self.encoded_datagram = ''
        self.buffer_size = 1024 #this is in bytes
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.size = 0

    def send_datagram(self, datagram):
        self.sock.sendto(datagram, (self.ip, self.port))

    def send_encoded_datagram(self):
        self.sock.sendto(self.encoded_datagram, (self.ip, self.port))

    def recieve_datagram(self):
        self.sock.bind((self.ip, self.port))
        #while True:
        data, addr = self.sock.recvfrom(self.buffer_size)
        #REPLACEprint("received message: \n", data)

    def recieve_encoded_datagram(self,sample_data,names):
        self.sock.bind((self.ip, self.port))
        self.gen_format_string(sample_data)
        counter = 0
        #while True: #y u do dis Dillan
        #REPLACEprint("Packet "+str(counter)+"\n")
        data, addr = self.sock.recvfrom(self.buffer_size)
        self.encoded_datagram = data
        self.decode_encoded_datagram()
        self.print_decoded_datagram(names)
        #REPLACEprint('\n')
        counter += 1

    def bindConnection(self):
        self.sock.bind((self.ip, self.port))
        f_u_python2 = 0

    def recieve_simple_encoded_datagram(self,sample_data,names):
        #self.sock.bind((self.ip, self.port))
        self.gen_format_string(sample_data)
        counter = 0
        #while True:
        #REPLACEprint("Packet "+str(counter)+"\n")
        data, addr = self.sock.recvfrom(self.buffer_size)
        self.encoded_datagram = data
        self.decode_simple_encoded_datagram()
        self.print_decoded_datagram(names)
        #REPLACEprint('\n')
        counter += 1

    def decode_encoded_datagram(self):
        self.decoded_datagram = unpack_from(self.format_string,self.encoded_datagram)

    def print_decoded_datagram(self,names):
        counter = 0
        for data in self.decoded_datagram:
            #REPLACEprint(names[counter]+': '+str(data)+'\n')
            counter += 1

    def decode_datagram(self,datagram):
        temp_array = []*len(self.size)
        for i in temp_array:
            self.decoded_datagram = unpack(self.format_string,datagram)

    def decode_simple_encoded_datagram(self):
        temp_decode = '' #store a compiled string in here
        decoded_array = []
        datagram = self.encoded_datagram
        datagram = datagram.decode()
        #print(datagram)
        for i in range(0,len(datagram)):
            if ',' in datagram[i]:
                decoded_array.append(temp_decode)
                temp_decode = ''
            else:
                temp_decode += datagram[i]
        self.decoded_datagram = decoded_array

    def gen_format_string(self,data):
        # Where Data is an array of values
        counter = 0
        for individual_thing in data:
            if self.what_type(individual_thing) == 'str':
                for s in range(0,len(individual_thing)):
                    self.format_string = self.format_string + 's'
            else:
                self.format_string = self.format_string + self.what_type(individual_thing)
            counter += 1
        #REPLACEprint("Your Format String: \n", self.format_string)
        self.size = counter

    def clear_format_string(self):
        self.format_string = ''

    def encode_datagram_hard(self,data):
        self.encoded_datagram = pack(self.format_string,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])

    def encode_datagram_simple(self,data):
        pack_str = ''
        for i in data:
            pack_str = pack_str + str(i) + ','
        self.encoded_datagram = pack_str.encode()

    def encode_datagram(self,data):
        strcount = 0
        counter = 0
        offset = 0
        num_str = 0
        temp_datagram = ''
        for i in range(0,len(self.format_string)):
            #REPLACEprint(self.format_string[i])
            if self.format_string[i] == 's':
                temp_datagram += str(pack(self.format_string[counter],data[i+offset+num_str][strcount].encode()))
                strcount += 1
                offset -= 1
            else:
                if strcount != 0:
                    num_str += 1
                    strcount = 0
                #print(offset)
                #print(data[i+offset+num_str])
                temp_datagram += str(pack(self.format_string[counter],data[i+offset+num_str]))

            counter += 1
        self.encoded_datagram = temp_datagram.encode()

    def what_type(self,invalue):
        value = str(type(invalue))[8:-2]
        #print(value)
        if value == "int":
            return 'i'
        elif value == "str":
            return 'str'
        elif value == "long":
            return 'l'
        elif value == "float":
            return 'f'
        elif value == "double":
            return 'd'
