import socket
import os
import time  # For performance timing
from analysis import NetworkAnalysis

network_analyzer = NetworkAnalysis() # Initialize the network analysis module

def upload_file(client_socket, file_path, gui):
    if not os.path.exists(file_path):
        gui.update_status(f"File not found: {file_path}")
        return

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Send metadata to the server
    client_socket.send(f"UPLOAD|{file_name}|{file_size}".encode('ascii'))

    # Open the file and send it in chunks
    start_time = time.time()
    with open(file_path, "rb") as file:
        while True:
            file_data = file.read(1024)
            if not file_data:
                break
            client_socket.send(file_data)

    end_time = time.time()
    transfer_time = end_time - start_time

    if transfer_time == 0:
        transfer_time = 1  # Set a minimum transfer time to avoid zero division

    transfer_rate = file_size / (1024 * 1024) / transfer_time  # MB/s

    gui.update_status(f"File '{file_name}' uploaded successfully.")
    gui.update_status(f"Transfer time is {transfer_time:.2f} seconds and transfer rate is {transfer_rate:.2f} MB/s")
    network_analyzer.log_event("Upload", file_name, file_size, transfer_time, transfer_rate)

def download_file(client_socket, file_name, save_path):
    try:
        # Request the file from the server
        client_socket.sendall(f"DOWNLOAD|{file_name}".encode())

        # Receive the server's response
        response = client_socket.recv(1024).decode()
        if response.startswith("ERROR"):
            print(f"Server: {response}")
            return

        # Parse file size
        file_size = int(response)
        client_socket.sendall("READY".encode())  # Notify server we're ready to receive

        # Track transfer start time
        start_time = time.time()
        received_size = 0

        # Open the file and write incoming chunks
        with open(save_path, "wb") as file:
            while received_size < file_size:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                file.write(chunk)
                received_size += len(chunk)

        # Log transfer completion
        transfer_time = time.time() - start_time
        transfer_rate = file_size / (1024 * 1024 * transfer_time)  # MB/s
        print(f"File '{file_name}' downloaded successfully to '{save_path}'.")
        print(f"Transfer time is {transfer_time:.2f} seconds and transfer rate is {transfer_rate:.2f} MB/s")
        network_analyzer.log_event("Download", file_name, file_size, transfer_time, transfer_rate)

    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")

    except Exception as e:
        print(f"Error during file download: {e}")


def delete_file(client_socket, file_name):
    client_socket.sendall(f"DELETE|{file_name}".encode())
    response = client_socket.recv(1024).decode()
    print(f"Server: {response}")


def list_directory(client_socket):
    client_socket.sendall("DIR".encode())
    response = client_socket.recv(4096).decode()
    print(f"Server Directory:\n{response}")


def create_subfolder(client_socket, path):
    client_socket.sendall(f"CREATE_SUBFOLDER|{path}".encode())
    response = client_socket.recv(1024).decode()
    print(response)


def delete_subfolder(client_socket, path):
    client_socket.sendall(f"DELETE_SUBFOLDER|{path}".encode())
    response = client_socket.recv(1024).decode()
    print(response)