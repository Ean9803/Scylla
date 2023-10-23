from asyncio.windows_events import NULL
from socket import *
import sys
import os

def safe_open_w(path, mode):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return open(path, mode)
    except:
        return None

def findip(host):
    try:
        ip = gethostbyname(host)
    except:
        ip = None
    return ip

if len(sys.argv) <= 1:
    print('Usage : "python Proxy.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(1)
tempfile = NULL
openedFile = False
isMainPage = False
WebFolder = ""
WebPage = ""

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    tcpCliSock.settimeout(15)
    print('Received a connection from:', addr)
    message = b''
    try:
        message = tcpCliSock.recv(1024)
    except:
        if (len(message) == 0):
            tcpCliSock.close()
            WebFolder = ""
            WebPage = ""
            print("End of page")
            continue
    print(message)
    # Extract the filename from the given message
    if (len(message) == 0):
        continue
    print(message.split()[1])
    filename = str(message).split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    isMainPage = False
    if findip(filename) is not None:
        isMainPage = True
        if not os.path.exists("./" + filename + "/"):
            os.makedirs("./" + filename + "/")
        WebFolder = "./" + filename + "/"
        WebPage = filename
    if (WebPage.__len__() == 0):
        continue
    try:
        # Check wether the file exist in the cache
        f = open(WebFolder + filetouse[1:], "r") 
        outputdata = f.read() 
        f.close();
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(outputdata.encode())
        
        print('Read from cache') 
        # Error handling for file not found in cache
    except IOError:
        if fileExist == "false": 
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            c.settimeout(15)
            print("Getting from ", WebPage)
            try:
                # Connect to the socket to port 80
                c.connect((WebPage, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                FileName = ""
                if not isMainPage:
                    FileName = filename
                c.send(("GET /" + FileName + " HTTP/1.1\r\nHost:" + WebPage + "\r\n\r\n").encode())
                # Read the response into buffer
                data = c.recv(10000)
                response = b""
                try:
                    while (len(data) > 0):
                        response += data
                        data = c.recv(10000)
                        print("READING length: ", len(data))
                except:
                    if (len(response) == 0):
                        raise Exception("No data retrived in time")
                # Create a new file in the cache for the requested file. 
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmp = safe_open_w(WebFolder + filename,"wb")
                if tmp is not None:
                    tmpFile = tmp
                    openedFile = True
                    print("WRITING TO FILE")
                    tmpFile.write(response)
                    tmpFile.close()
                print("RELAYING")
                tcpCliSock.send(response)
            except Exception as e:
                print(str(e))
                if openedFile:
                    tmpFile.close()
                if os.path.exists(WebFolder + filename):
                    os.remove(WebFolder + filename)
                    print("removed file")
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            tcpCliSock.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
    # Close the client and the server sockets 
    tcpCliSock.close()
tcpCliSock.close()