import socket
import os

def upload_file(client_socket, file_path):
    #handles the error in case that the file cannot be found
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    #this sends the file's metadata
    client_socket.sendall(f"UPLOAD|{file_name}|{file_size}".encode())

    #read and send the file content
    with open(file_path, "rb") as file:
        while (chunk := file.read(4096)):
            client_socket.sendall(chunk)
    print(f"File '{file_name}' uploaded successfully.")

def download_file(client_socket, file):
    if not os.path.exists(file):
        print(f"File not found: {file}")
        return

def delete():



