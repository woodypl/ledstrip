import SocketServer
import socket
import struct
import threading
import time
from raspledstrip.ledstrip import *

HOST = '0.0.0.0'
PORT = 8000

strip = LEDStrip(8)
hbevent = threading.Event()

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

def heartbeat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while hbevent.is_set():
        data = "PiStrip live on {0}".format(PORT)
	sock.sendto(data, ('<broadcast>', 55555))
	time.sleep(30)
		

if __name__ == "__main__":
	server = SocketServer.TCPServer((HOST, PORT), StripTCPHandler)
	keepalive = threading.Thread(target=heartbeat)
	hbevent.set()
	keepalive.start()
	print "Will serve on {0}:{1}".format(HOST,PORT)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print "Please allow 30 seconds to terminate"
		hbevent.clear()
		keepalive.join()
