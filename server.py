#server.py

#importing libraries
import sys,os
import socket


def create_socket(socket_type, name_of_port):
    '''
        Creating a socket in IPV4 family of the type received as argument to function
    '''
    new_socket = socket.socket(socket.AF_INET, socket_type)
    new_socket.bind(("", 0))
        #gives an available server socket port
    print ("{}={}".format(name_of_port, new_socket.getsockname()[1]))
    return new_socket

def server_udp_negotiation(n_socket, req_code):
    '''
        #Negotiation stage using UDP sockets, receivbes request code and validates it then sends r_port in passive mode and receives r_port in activ emode from client
    '''
    while True:
        print("WAITING FOR CLIENT REQUEST CODE")
        a, b = n_socket.recvfrom(1024)
        client_r, client_address = a, b
        client_r = client_r.decode('utf-8')
                #to differentiate between active and passive mode , req_code and r_port are space separaeted in message from client in active mode
        if ' ' in client_r:
            mode = 'A'
            client_req_code, client_r_port = client_r.split(' ')
            client_req_code = int(client_req_code)

                #req_code received from client to validate
        else:
            mode = 'P'
            client_req_code = int(client_r)

        print("CLIENT REQUEST CODE RECEIVED: " + str(client_req_code))
        if client_req_code == req_code:
            print("CLIENT REQUEST CODE VERIFIED")

            if mode == 'P':
                        #to send r_port to client to connect to for file transfer in passive mode
                        #creating a TCP socket used in transaction stage
                r_socket = create_socket(socket.SOCK_STREAM, "SERVER_TCP_PORT")
                r_port = r_socket.getsockname()[1]
                print("WAITING FOR CLIENT TRANSACTION PORT CONFIRMATION")
                n_socket.sendto(str(r_port).encode('utf-8'), client_address)
                a, b = n_socket.recvfrom(1024)
                client_r_port, client_address = int(a), b
                if client_r_port == r_socket.getsockname()[1]:
                    print("CLIENT CONFIRMED TRANSACTION PORT")
                    n_socket.sendto("ok".encode('utf-8'), client_address)
                    return mode,r_socket,client_r_port,client_address
                else:
                    print("CLIENT FAILED TO CONFIRM TRANSACTION PORT")
                    n_socket.sendto("no".encode('utf-8'), client_address)

            if mode == 'A':
                n_socket.sendto("1".encode('utf-8'), client_address)
                r_socket = create_socket(socket.SOCK_STREAM, "SERVER_TCP_PORT")
                return mode,r_socket,client_r_port,client_address

        else:
            print("CLIENT REQUEST CODE INVALID")
            n_socket.sendto("-1".encode('utf-8'), client_address)

def server_tcp_transaction_passive(r_socket,file_to_send):
    '''
        TCP transaction stage for passive mode
    '''
    print("WAITING FOR TRANSACTION FROM CLIENT")
        #listening to 1 queued message
    r_socket.listen(1)
    connection_socket, client_address = r_socket.accept()
        #opening file in the current working irectory
    f = open(os.path.join(sys.path[0], file_to_send),'rb')
    l = f.read(1024)
    while (l):
       connection_socket.send(l)
       #print('Sent ',repr(l))
       l = f.read(1024)
    f.close()
    completion_msg = "File Sent"
    connection_socket.send(completion_msg.encode('utf-8'))
    print("REPLIED TO CLIENT, TRANSACTION ENDED")
    connection_socket.close()
    r_socket.close()

def server_tcp_transaction_active(r_socket,client_r_port,client_address,file_to_send):
    '''
        TCP transaction stage for active mode
    '''
        #server initiates connection in active mode so getting client ip and port to connect on
    client_ip = client_address[0]
    #replace with client_ip
    print(client_ip,client_r_port)
    r_socket.connect((client_ip,int(client_r_port)))
    #r_socket.connect(('127.0.0.1',int(client_r_port)))
    print("CONNECTION INITIATED FROM SERVER")
        #sending file from current working directory
    f = open(os.path.join(sys.path[0], file_to_send),'rb')
    l = f.read(1024)
    while (l):
       r_socket.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()
    completion_msg = "File Sent"
    r_socket.send(completion_msg.encode('utf-8'))
    print("REPLIED TO CLIENT, TRANSACTION ENDED")
    r_socket.close()


def main():
    '''
        Argumemts:
                req_code        : secret integer code for authorization in negotiation stage
                file_to_send: name of file to be sent
    '''
    try:
        req_code = int(sys.argv[1])
        file_to_send = str(sys.argv[2])
    except IndexError:
        print("MISSING PARAMETER(S), <REQ_CODE><FILE_TO_SEND> TRY AGAIN")
        sys.exit(1)
    except ValueError:
        print("PARAMETER TYPE WRONG, TRY AGAIN")
        sys.exit(1)
    n_socket = create_socket(socket.SOCK_DGRAM, "SERVER_PORT")
    while True:
        mode,r_socket,client_r_port,client_address = server_udp_negotiation(n_socket, req_code)
        if mode == 'P':
            server_tcp_transaction_passive(r_socket,file_to_send)
        else:
            server_tcp_transaction_active(r_socket,client_r_port,client_address,file_to_send)

if __name__ == "__main__":
    main()

