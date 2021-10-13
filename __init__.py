import socket
import json
import threading
import time

s = socket.socket()
host = '0.0.0.0'
port = 8080
ThreadCount = 0
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

print('hello')
print('Socket is listening..')
s.listen(5)
print(socket.gethostbyname(socket.gethostname()))


clients = [] # The clients we have connected to


def recvall(sock, n):
    data = ""
    while True:
        new = sock.recv(n).decode()
        find = new.find('$$over$$')
        if find != -1 :
            data += new[0:find]
            return data
        data += new  


def send_all(sock,data):
    data += "$$over$$"  
    sock.sendall(data.encode())
    print('sending to' + str(sock))


def clientthread(conn, addr, pseudo):
     
    # sends a message to the client whose user object is conn
    id = len(clients)-1
    msg = "Welcome " + pseudo +" "+str(addr[1])
    conn.send(msg.encode())

    while True:
            try:
                data = recvall(conn,128)
                if data:
                    print('received')
                    data = json.loads(data)
                    client = data['client']
                    msg = data['msg']
                    send(int(client),msg, id)
                else:
                    pass
 
            except:
                continue
 
 
"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def send(to, msg, exped):
    exped = clients[exped]["pseudo"]
    data = json.dumps({"from":exped, "msg":msg})
    send_all(clients[to]["conn"],data)


while True:
 
    conn, addr = s.accept()
    pseudo = conn.recv(32).decode()
    clients.append({"conn" : conn, "pseudo" : pseudo})
 
    # prints the address of the user that just connected
    print (addr[0] + " connected")
 
    # creates and individual thread for every user
    # that connects
    threading.Thread(target=clientthread,args=(conn,addr, pseudo)).start()    
 
conn.close()
server.close()