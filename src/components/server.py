import socket
import os
import threading
import time  # For performance timing

host = '127.0.0.1'
port = 3300
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


def send_file(client_socket, file_name):
    if not os.path.exists(file_name):
        client_socket.sendall("ERROR: File not found".encode())
        return

    file_size = os.path.getsize(file_name)
    client_socket.sendall(f"{file_size}".encode())  # Send file size to the client

    try:
        response = client_socket.recv(4096).decode()
        if response != "READY":
            print(f"Client not ready for file transfer. Received: {response}")
            return

        # Track transfer start time
        start_time = time.time()
        with open(file_name, "rb") as file:
            while chunk := file.read(4096):
                client_socket.sendall(chunk)

        # Log transfer completion
        transfer_time = time.time() - start_time
        print(f"File '{file_name}' sent successfully in {transfer_time:.2f} seconds.")

    except Exception as e:
        print(f"Error sending file '{file_name}': {e}")



def receive(client_socket):
    print("Recieving...")
    try:
        # Receive the command from the client
        try:
            data = client_socket.recv(1024).decode()
        except ConnectionResetError:
            print("Client disconnected abruptly.")
            return

        print(f"Received command: {data}")

        if data.startswith("UPLOAD"):
            _, file_name, file_size = data.split("|")
            file_size = int(file_size)

            client_socket.sendall("PROCEED".encode())

            start_time = time.time()
            with open(file_name, "wb") as file:
                received = 0
                while received < file_size:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    file.write(chunk)
                    received += len(chunk)

            transfer_time = time.time() - start_time
            print(f"File '{file_name}' received successfully in {transfer_time:.2f} seconds.")

        elif data.startswith("DOWNLOAD"):
            _, file_name = data.split("|")
            send_file(client_socket, file_name)

        elif data.startswith("DELETE"):
            _, file_name = data.split("|")
            if os.path.exists(file_name):
                os.remove(file_name)
                client_socket.sendall("File deleted successfully.".encode())
            else:
                client_socket.sendall("ERROR: File not found".encode())

        elif data == "DIR":
            dir_listing = os.listdir(".")
            if dir_listing:
                client_socket.sendall("\n".join(dir_listing).encode())
            else:
                client_socket.sendall("Directory is empty.".encode())
                
        elif data.startswith("CRT_DIR"):
            print("Command Recieved - Creating Directory")
            client_socket.sendall("Created Directory".encode())
            
        elif data.startswith("DEL_DIR"):
            client_socket.sendall("Deleting Directory".encode())

        else:
            client_socket.sendall("ERROR: Unknown command".encode())
            

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def main():
    print("Server is running...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        thread = threading.Thread(target=receive, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()