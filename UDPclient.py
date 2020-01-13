#Eli Decker
#CS331 Project 4
# November 12, 2019
import time
import sys
import socket

def show_summary(timeStart, host, pingCounter, pingsReceived, minPing, avgPing, maxPing):
    total_time = (time.time() - timeStart) * 1000

    print('--- %s localhost ping statistics ---' % (host))
    # print('%d packets transmitted, %d received, %0.5f%% packet loss' % (pingCounter, pingsReceived, (pingCounter - pingsReceived) / pingCounter * 100))
    print('round-trip min/avg/max/stddev = %0.10f/%0.10f/%0.10f/%0.10f ms' % (minPing, avgPing / pingCounter, maxPing, maxPing - minPing))
    sys.exit()

def main(argv):
    host = "localhost"
    numPings = sys.maxsize
    timeout = 0.055

    port = 12345

    minPing = 999999
    maxPing = 0
    pingCounter = 0
    pingsReceived = 0
    avgPing = 0

    minPingMessage = 999999
    maxPingMessage = 0
    pingMessageCounter = 0
    pingMessageReceived = 0
    avg = 0


    message_bytes = 256
    message = 'This is the message.  It will be repeated.'
    print('sending "%s"' % message)
    # sock.sendall(str.encode(message))

    # get input for host name, timeout value, and number of pings
    temphost = input("Enter host (default: localhost): ")
    if temphost != '':
        host = temphost
    
    tempTimeout = input("Enter timeout value in seconds (default: 0.055): ")
    if tempTimeout != '':
        timeout = float(tempTimeout)
    
    tempNumPings = input("Enter number of pings (default: forever): ")
    if tempNumPings != '':
        numPings = int(tempNumPings)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # start the time calculation
    timeStart = time.time()


    for seq in range(numPings):
        try:
            startTime = time.time()
            amount_received = 0
            amount_expected = len(message)
            clientSocket.sendto(str.encode(message), (host, port))
            while amount_received < amount_expected:
                start = time.time()
                data, server = clientSocket.recvfrom(8000)
                # data = data.decode()
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
            
            endTime = time.time()
            elapsed = (endTime - startTime) * 1000
            if elapsed < minPingMessage: 
                minPingMessage = elapsed
            if elapsed > maxPingMessage: 
                maxPingMessage = elapsed
            avg += elapsed
            pingMessageCounter += 1
            pingMessageReceived += 1
            amount_received += len(data)
            print(elapsed)

        except socket.timeout as e:
            print('seq=%d REQUEST TIMED OUT' % (seq))
            pingCounter+=1
        except KeyboardInterrupt: #listen for ctrl - c to stop ping and show the output stats
            print('\n')
            show_summary(timeStart, host, pingCounter, pingsReceived, minPing, avgPing, maxPing)

    show_summary(timeStart, host, pingCounter, pingsReceived, minPing, avgPing, maxPing)


if __name__ == "__main__":
    main(sys.argv)