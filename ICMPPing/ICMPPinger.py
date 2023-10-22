from socket import *
import socket as sck
import os
import sys
import struct
import time
import select
import binascii 
ICMP_ECHO_REQUEST = 8

def checksum(string):
    # In this function we make the checksum of our packet 
    string = bytearray(string)
    csum = 0
    countTo = (len(string) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(string):
        csum = csum + string[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    global mintime, maxtime, sumtime, count
    while 1: 
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out. (0)"
        timeReceived = time.time()

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out. (1)"

        recPacket, addr = mySocket.recvfrom(1024)
 
        type, code, checksum, id, seq = struct.unpack('bbHHh', recPacket[20:28])
        bytesInDouble = struct.calcsize("d")
        send_time = struct.unpack('d', recPacket[28:28 + bytesInDouble])[0]
        
        rtt = (timeReceived - send_time) * 1000
        count += 1
        sumtime += rtt
        mintime = min(mintime, rtt)
        maxtime = max(maxtime, rtt)

        ip_header = struct.unpack('!BBHHHBBH4s4s' , recPacket[:20])
        ttl = ip_header[5]
        saddr = sck.inet_ntoa(ip_header[8])
        length = len(recPacket) - 20

        return ("{} bytes from {}: icmp_seq={} ttl={} time={:.3f} ms".format(length, saddr, seq, ttl, rtt))

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(str(header + data))

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum((header + data))
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout): 
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    global mintime, maxtime, sumtime, count
    mintime = float('+inf')
    maxtime = float('-inf')
    sumtime = 0
    count = 0
    cnt = 0

    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Send ping requests to a server separated by approximately one second
    for i in range(0, 5):
        cnt += 1
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)# one second
    if cnt != 0:
        print(host + " ping results:")
        print("{} packets transmitted, {} packets received, {:.1f}% lost".format(cnt, count, 100.0 - count * 100.0 / cnt))
        if count != 0:
            print("rtt: [min = {:.3f} | avg = {:.3f} | max = {:.3f} ms]\n\n".format(mintime, sumtime / count, maxtime))
        else:
            print("\n\n")
    return delay

ping("127.0.0.1")
ping("www.ox.ac.uk")
ping("www.uq.edu.au")
ping("www.kyoto-u.ac.jp")
ping("www.up.ac.za")