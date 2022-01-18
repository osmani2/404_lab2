#!/usr/bin/env python3
import socket, multiprocessing 
import time

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# send and recieve from multiple clients
def multi_echo(addr, conn):
    print("Connected by", addr)

    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    print(full_data)
    time.sleep(0.5)
    conn.sendall(full_data)

    # remember to shut down before clossing
    conn.shutdown(socket.SHUT_WR)
    
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            # start a process to handle multiple connections
            process = multiprocessing.Process(target=multi_echo, args=(addr,conn))
            process.daemon = True
            process.start()
           

if __name__ == "__main__":
    main()
