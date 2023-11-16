#import socket module
import datetime
from socket import *
import sys # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverSocket.bind(('', 12000))
serverSocket.listen(1)
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        if len(message) > 0:
            filename = message.split()[1] 
            f = open(filename[1:]) 
            outputdata = f.read()
            now  = datetime.datetime.now()
            statusLine = "HTTP/1.1 200 OK\r\n"
            headerInfo = {"Date":now.strftime("%Y-%m-%d%H:%M:%S"),
                          "Content-Type":"text/html",
                          "Charset=": "uuiltf-8",
                          "Content-Length": len(outputdata),
                          "Keep-Alive": "timeout=%d,Max%d"%(10,100),
                          "Connection": "Keep-Alive:"}
            headerLines = "\r\n".join("%s:%s"%(item, headerInfo[item]) for item in headerInfo)
            HTTPResponse = statusLine + headerLines + "\r\n\r\n"
            connectionSocket.send(HTTPResponse.encode())
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
 
            connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data