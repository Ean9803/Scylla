from socket import *
import base64
import ssl

def Email():
    username =  "vs2022test2023@gmail.com"
    key = "vfhr xprb sexh opwy"
    base64_str = ("\x00"+username+"\x00"+key).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    clientSocket.send(authMsg)
    recv_auth = clientSocket.recv(1024)
    print(recv_auth.decode())

    # Send MAIL FROM command and print server response.
    mailFrom = "MAIL FROM: <vs2022test2023@gmail.com> \r\n"
    clientSocket.send(mailFrom.encode())
    recvCode = clientSocket.recv(1024).decode()
    if recvCode[:3] != '250':
        print('250 reply not received from server.')
        clientSocket.close()
    else:
        # Send RCPT TO command and print server response.
        sendto = input("Enter recipient: ")
        rcptTo = "RCPT TO: <" + sendto + "> \r\n"
        clientSocket.send(rcptTo.encode())
        recvCode = clientSocket.recv(1024).decode()
        if recvCode[:3] != '250':
            print('250 reply not received from server.')
            clientSocket.close()
        else:
            # Send DATA command and print server response.
            data = "DATA\r\n"
            clientSocket.send(data.encode())
            recvCode = clientSocket.recv(1024).decode()
    
            # Send message data.
            sub = input("Enter subject: ")
            subject = "Subject: " + sub + " \r\n\r\n" 
            clientSocket.send(subject.encode())
            message = input("Enter message: \r\n")
            clientSocket.send(message.encode())
            clientSocket.send(endmsg.encode())

            # Send QUIT command and get server response.
            clientSocket.send("QUIT\r\n".encode())
            message=clientSocket.recv(1024).decode()
            print("\n\n[MESSAGE SENT]")
            clientSocket.close()

endmsg = "\r\n.\r\n"
mailserver = ("smtp.gmail.com", 465) #Fill in start #Fill in end
Socket = socket(AF_INET, SOCK_STREAM)
Socket.settimeout(1)
clientSocket = ssl.wrap_socket(Socket)
clientSocket.connect(mailserver)
recv = clientSocket.recv(1024)
recv = recv.decode()
print("Message after connection request:" + recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
    clientSocket.close()
else:
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recvInit = clientSocket.recv(1024)
    recvInit = recvInit.decode()
    print("Message after HELO command:" + recvInit)
    if recvInit[:3] != '250':
        print('250 reply not received from server.')
        clientSocket.close()
    else:
        Email()