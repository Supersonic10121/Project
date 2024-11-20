import socket

#HOST = socket.gethostbyname(socket.gethostname())
#will not work in virtual but should get the ip adress of the client 



#need to make a while loop to run everything 

#server  has different modes for recive and transfer mode 





import socket 
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 2300))


Username = ""


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'UN':
                Username = input("Please type your username")
                client.send(Username.encode('ascii'))
            else:
                print(message)






        
        except:
            print("An error occured")
            client.close()
            break



receive_thread = threading.Thread(target=receive)
receive_thread.start()