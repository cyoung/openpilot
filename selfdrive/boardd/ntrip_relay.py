import zmq
import time
import json
import socket
import sys


context = zmq.Context()
ubloxRawSend_socket = context.socket(zmq.PUB)
ubloxRawSend_socket.bind ("tcp://*:8069")

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('0.0.0.0', 8090)

print >>sys.stderr, 'starting up on %s port %s' % server_address

sock.bind(server_address)

sock.listen(1)


while 1:
  print >>sys.stderr, 'waiting for a connection'
  connection, client_address = sock.accept()
  try:
      print >>sys.stderr, 'connection from', client_address

      # Receive the data in small chunks and retransmit it
      while True:
          data = connection.recv(512)
          print >>sys.stderr, 'received %d' % len(data)
          if data:
              print >>sys.stderr, 'sending data back to the gps'
              ubloxRawSend_socket.send(data)
          else:
              print >>sys.stderr, 'no more data from', client_address
              break
            
  finally:
      # Clean up the connection
      connection.close()





#ubloxRawSend_socket.send(b'\xB5\x62\x0A\x04\x00\x00\x0E\x34')
#time.sleep(5)