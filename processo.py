import socket
import sys
import time

# Tamanho da mensagem fixa em bytes
F = 10

def main(process_id, num_repetitions, delay):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    
    for _ in range(int(num_repetitions)):
        request_msg = f"REQUEST|{process_id}".ljust(F)
        client_socket.send(request_msg.encode('utf-8'))
        
        grant_msg = client_socket.recv(F).decode('utf-8')
        
        if "GRANT" in grant_msg:
            print(f"Process {process_id} granted access")
            
            with open('resultado.txt', 'a') as file:
                file.write(f"Process {process_id}: {time.time()}\n")
            
            time.sleep(int(delay))
        
        release_msg = f"RELEASE|{process_id}".ljust(F)
        client_socket.send(release_msg.encode('utf-8'))
    
    client_socket.close()

if __name__ == "__main__":
    process_id = sys.argv[1]
    num_repetitions = sys.argv[2]
    delay = sys.argv[3]
    main(process_id, num_repetitions, delay)
