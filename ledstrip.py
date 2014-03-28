import SocketServer
import socket
import struct
from raspledstrip.ledstrip import *

HOST = '0.0.0.0'
PORT = 8000

strip = LEDStrip(8)

class StripTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		while self.request.recv(1) == b'\xff':
			data = self.request.recv(7, socket.MSG_WAITALL)
			if data[0] == '!':
				strip.update()
			elif data[0] == '=':
				num = 10*int(data[2])+int(data[3])
				strip.setRGB(num, struct.unpack("B", data[4])[0], struct.unpack("B", data[5])[0], 
						struct.unpack("B", data[6])[0])
			else:
				self.request.sendall("Unknown command!")

if __name__ == "__main__":
	server = SocketServer.TCPServer((HOST, PORT), StripTCPHandler)
	print "Will serve on {0}:{1}".format(HOST,PORT)
	server.serve_forever()
