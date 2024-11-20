#test

#trying to modify server to multithred 


import socket

host = '10.142.0.2'
port = 3300
BUFFER_SIZE = 1024
dashes = '----> '

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp: # sock stream is a TCP connection
    server_tcp.bind((host,port))

    while True:
        server_tcp.listen(6)  # the number here is teh ammount of conmections being lisitened for 
        print('[*] Waiting for connection')

        connection, addr = server_tcp.accept()
        with connection:
            print(f'[*] Established cpnnection from IP {addr[0]} port: {addr[1]}')
            while True:
                data = connection.recv(BUFFER_SIZE)
            if not data:
                break
            else:
                print('[*] Data received: {}'.format(data.decode('utf-8')))
            connection.send(dashes.encode('utf-8') + data)