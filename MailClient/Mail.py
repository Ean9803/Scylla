from socket import *
import base64
import ssl

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
heloCommand = 'EHLO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
recv1 = recv1.decode()
print("Message after EHLO command:" + recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

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
recv2 = clientSocket.recv(1024).decode()
print("After MAIL FROM command: " + recv2)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <irobot9803@gmail.com> \r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024).decode()
print("After RCPT TO command: " + recv3)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode()
print("After DATA command: " + recv4)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send message data.
subject = "Subject: SMTP mail client testing \r\n\r\n" 
clientSocket.send(subject.encode())
message = input("Enter your message: \r\n")
clientSocket.send(message.encode())
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024)
print("Response after sending message body:" + recv_msg.decode())
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
clientSocket.send("QUIT\r\n".encode())
message=clientSocket.recv(1024).decode()
print (message)
clientSocket.close()