import socket
import threading
import queue
import time

F = 10
request_queue = queue.Queue()
access_count = {}
log_lock = threading.Lock()

def handle_request(client_socket, client_address):
    while True:
        message = client_socket.recv(F).decode('utf-8').strip()
        
        if not message:
            break
        
        current_time = time.strftime("%H:%M:%S.%f", time.localtime())
        log_message = f"[{current_time}] Received: {message}"
        print(log_message)
        
        with log_lock:
            log_file = open("coordinator_log.txt", "a")
            log_file.write(log_message + "\n")
            log_file.close()
        
        if message.startswith("REQUEST"):
            process_id = message.split("|")[1].strip()
            with log_lock:
                request_queue.put(process_id)
                
            if process_id == request_queue.queue[0]:
                client_socket.send(f"GRANT|{process_id}".ljust(F).encode('utf-8'))
                with log_lock:
                    access_count[process_id] = access_count.get(process_id, 0) + 1
                    
                    log_message = f"[{current_time}] Granted access to process {process_id}. Current count: {access_count[process_id]}"
                    print(log_message)
                    with log_lock:
                        log_file = open("coordinator_log.txt", "a")
                        log_file.write(log_message + "\n")
                        log_file.close()
        
        elif message.startswith("RELEASE"):
            process_id = message.split("|")[1].strip()
            with log_lock:
                request_queue.get()
                
            if not request_queue.empty():
                next_process_id = request_queue.queue[0]
                client_socket.send(f"GRANT|{next_process_id}".ljust(F).encode('utf-8'))
                
                log_message = f"[{current_time}] Released access for process {process_id}. Next process in line: {next_process_id}"
                print(log_message)
                with log_lock:
                    log_file = open("coordinator_log.txt", "a")
                    log_file.write(log_message + "\n")
                    log_file.close()
        
        client_socket.send(f"ACK|{message}".ljust(F).encode('utf-8'))

    client_socket.close()

def interface_thread():
    while True:
        command = input("Enter command (1: print queue, 2: print access count, 3: exit): ")
        
        if command == "1":
            with log_lock:
                print(f"Queue: {list(request_queue.queue)}")
                log_message = f"[{time.strftime('%H:%M:%S.%f', time.localtime())}] Printed queue: {list(request_queue.queue)}"
                print(log_message)
                with log_lock:
                    log_file = open("coordinator_log.txt", "a")
                    log_file.write(log_message + "\n")
                    log_file.close()
        
        elif command == "2":
            with log_lock:
                print(f"Access Count: {access_count}")
                log_message = f"[{time.strftime('%H:%M:%S.%f', time.localtime())}] Printed access count: {access_count}"
                print(log_message)
                with log_lock:
                    log_file = open("coordinator_log.txt", "a")
                    log_file.write(log_message + "\n")
                    log_file.close()
        
        elif command == "3":
            print("Shutting down coordinator.")
            log_message = "[2023-01-01 00:00:00.000000] Coordinator shutting down."
            print(log_message)
            with log_lock:
                log_file = open("coordinator_log.txt", "a")
                log_file.write(log_message + "\n")
                log_file.close()
            exit(0)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(5)

    threading.Thread(target=interface_thread).start()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_request, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
