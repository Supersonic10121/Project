import threading
import socket

host = '127.0.0.1' # local host IP
port = 2300


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#define different functions for file upload or download 

Username = "Test"
PW = "1234"



def recive():
    while True:
        client, adress = server.accept() # accept connection
        print("Connected with {}".format(str(client)))
        #print("Connected with {}".format(str(address)))
        
        #ask for username and password
        client.send('UN'.encode('ascii')) # the code is not waiting for a response from the user yet I think 
        print("The user sent ")
        print(adress.recive(1024).decode('ascii'))

        if(adress.recive(1024).decode('ascii') == Username):
            print("worked")


recive()


#currently avaible files need to be sent to user 
















































""""
def main_function():

    while True:
        connection, addr = server_tcp.accept()
        print("Connection recived with : {addr}")

        thread = threading.Thread(target=handle, args= addr)
        thread.start()


main_function()"""