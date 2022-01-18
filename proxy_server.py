# connect to Google
#!/usr/bin/env python3
import socket, sys, multiprocessing
import time

#define address & buffer size
HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip


# send and recieve from multiple clients
def multi_proxy(addr, conn):
    host = 'www.google.com'
    port = 80

    print("Connected by", addr)

    # ACTS AS A CLIENT
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_server:

        # Socket, IP, connect
        print("Connected by Google")
        remote_ip = get_remote_ip(host)
        proxy_server.connect((remote_ip , port))
        print (f'Socket Connected to {host} on ip {remote_ip}')
        
        #recieve data from client and send back to google
        full_data = conn.recv(BUFFER_SIZE)
        print(full_data)
        time.sleep(0.5)
        proxy_server.sendall(full_data)

        # Remember to shutdown
        # No further intent to read or write, closes socket connection
        proxy_server.shutdown(socket.SHUT_WR)

        # recieve data from google, send to client
        data = proxy_server.recv(BUFFER_SIZE)
        conn.send(data)
        
    # remember to shut down before clossing
    conn.shutdown(socket.SHUT_WR)
    conn.close()

def main():
    # ACTS AS A SERVER
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
            process = multiprocessing.Process(target=multi_proxy, args=(addr,conn))
            process.daemon = True
            process.start()

if __name__ == "__main__":
    main()
