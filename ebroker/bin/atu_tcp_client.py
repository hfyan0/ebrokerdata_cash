#!/usr/bin/python
from socket import socket
from select import select

# Blocking mode to readline
def readlines(sock, recv_buffer=4096, delim='\n'):
	buffer = ''
	data = True
	while data:
		data = sock.recv(recv_buffer)
		buffer += data

		while buffer.find(delim) != -1:
			line, buffer = buffer.split('\n', 1)
			yield line
	return
def non_blocking_readlines(sock, isContinueReading, recv_buffer=4096, delim='\n'):
	sock.setblocking(False)
	isSocketOpened = True
	pending_data = ''
	while True and isSocketOpened and isContinueReading():
		#print "Checking..."
		readable, writable, exceptional = select([sock], [], [sock], 1)

		if readable:
			#print "Readable..."
			buffer = sock.recv(recv_buffer)
			if (len(buffer) == 0):
				isSocketOpened = False
			else:
				pending_data += buffer
				while pending_data.find(delim) != -1:
					line, pending_data = pending_data.split(delim, 1)
					#print "line=", line
					yield line

	print "socket disconnected"
	isSocketOpened = False
#	sock.shutdown(socket.SHUT_RDWR)
	sock.close()


