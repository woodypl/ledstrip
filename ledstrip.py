import SocketServer



class StripTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		if self.request.recv(1) != b'\xff':
			return
		data = self.request.recv(7, socket.MSG_WAITALL)
		print data

if __name__ == "__main__":
	server = SocketServer.TCPServer((HOST, PORT), StripTCPHandler)
	server.serve_forever()
