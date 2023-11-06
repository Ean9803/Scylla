from socket import *
import time
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1)
for i in range(1,10):
    starttime=time.time()
    msg='ping:'+str(i)
    print(msg)
    try:
        clientSocket.sendto(msg.encode(),(serverName,serverPort))
        msg,server = clientSocket.recvfrom(4096)
        elapsed=time.time()-starttime
        print("message got: ", msg.decode())
        print("Elapsed time", elapsed)
    except Exception as error:
        print('msg time out')
   
clientSocket.close() 
    
