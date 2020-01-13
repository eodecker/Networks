#Eli Decker
# CS331 
# Project 5
# TCPclient.py

import socket
import sys
import time


def main(argv):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    host = 'localhost'

    # get input for host name, timeout value, and number of pings
    temphost = input("Enter host (default: localhost): ")
    if temphost != '':
        host = temphost
        
    server_address = (host, 10000)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    minPing = 999999
    maxPing = 0
    avgPing = 0
    pingCounter = 0
    pingsReceived = 0

    try:
        
        # Send data
        message = 'This is the message.  It will be repeated.'
        print('sending "%s"' % message)
        sock.sendall(str.encode(message))

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            start = time.time()
            data = sock.recv(16).decode()
            end = time.time()
            elapsed = (end - start) * 1000
            if elapsed < minPing: 
                minPing = elapsed
            if elapsed > maxPing: 
                maxPing = elapsed
            avgPing += elapsed
            pingCounter += 1
            pingsReceived += 1
            amount_received += len(data)
            print('received "%s"' % data)

    finally:
        print('closing socket')
        print('--- %s localhost ping statistics ---' % (host))
        print('%d packets transmitted, %d received, %0.5f%% packet loss' % (pingCounter, pingsReceived, (pingCounter - pingsReceived) / pingCounter * 100))
        print('round-trip min/avg/max/stddev = %0.10f/%0.10f/%0.10f/%0.10f ms' % (minPing, avgPing / pingCounter, maxPing, maxPing - minPing))
        print("Total Time = %0.10f ms" %(avgPing))
        sock.close()

if __name__ == "__main__":
    main(sys.argv)