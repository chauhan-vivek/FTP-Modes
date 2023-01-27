#client.py

#importing libraries
import sys,os
import socket

#client_r_port = "42289"


def client_udp_negotiation_active(server_address, n_port, req_code):
    '''
        Negotion using UDP socket for active mode: In this stage sends a dynamic r_port and req_code to server
        Waits for an acknowledgement from server to procceed to transaction stage
    '''
    try:
                #creating a UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("INITIATING NEGOTIATION WITH REQUEST CODE AND SENDING R_PORT: ")
                #r_port is attached to TCP socket
        client_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #binding to available port
        client_socket_a.bind(('',0))
                #getting an empty port in local machine
        client_r_port = client_socket_a.getsockname()[1]
        print("[CLIENT R_PORT IS : ]",client_r_port)
        client_r = str(req_code) + ' ' + str(client_r_port)
        client_socket.sendto(str(client_r).encode('utf-8'),
                             (server_address, n_port))
        ack = int(client_socket.recvfrom(1024)[0])
        if ack == 0:
            print("REQUEST CODE IS INVALID")
            sys.exit(1)
        if ack == 1:
            print("REQUEST CODE VERIFIED")
            return client_socket_a
    except socket.error as e:
        print("CONNECTION ERROR: " + str(e))
        sys.exit(1)


def client_tcp_transaction_active(client_socket_a, file_received):
    '''
        Transaction using TCP socket for active mode: In this stage client binds to a r_port waiting for file contents to be received from server
    '''
    print("CLIENT WAITING FOR TRANSACTION")
    #client_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket_a.bind(('',int(client_r_port)))
        #in active mode server initiates a connection request so listening to one message in queue buffer
    client_socket_a.listen(1)
    conn_socket, server_add = client_socket_a.accept()

        #Receiving file ans writing the file in current directory with the file name supplied as argument
    #while True:
    with open(os.path.join(sys.path[0],file_received), 'wb') as f:
        print('receiving data...')
        data = conn_socket.recv(1024)
        print(data)
        # write data to a file
        f.write(data)
    f.close()
    print('Successfully got the file')
    client_rcv_msg = (conn_socket.recv(1024)).decode('utf-8')
    return client_rcv_msg


def client_udp_negotiation_passive(server_address, n_port, req_code):
    '''
        Negotion using UDP socket for passive mode: In this stage sends a req_code to validate with server
        Receives r_port from server to be used in transaction stage
    '''
    try:
                #creating UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("INITIATING NEGOTIATION WITH REQUEST CODE: " + str(req_code))
        print(server_address, n_port)
        client_socket.sendto(str(req_code).encode('utf-8'),
                             (server_address, n_port))
        #receiving r_port from server
        r_port = int(client_socket.recvfrom(1024)[0])
        if r_port == -1:
            print("REQUEST CODE IS INVALID")
            sys.exit(1)
        print("TRANSACTION PORT NEGOTIATED: " + str(r_port))
        print("CONFIRMING TRANSACTION PORT WITH SERVER")
        client_socket.sendto(str(r_port).encode('utf-8'),
                             (server_address, n_port))
        ack = (client_socket.recvfrom(1024)[0]).decode('utf-8')
        if ack == "ok":
            print("TRANSACTION PORT CONFIRMATION ACKNOWLEDGED")
            return r_port
        else:
            print("TRANSACTION PORT CONFIRMATION FAILED")
            sys.exit(1)
    except socket.error as e:
        print("CONNECTION ERROR: " + str(e))
        sys.exit(1)


def client_tcp_transaction_passive(server_address, r_port, file_received):
    '''
        Transaction using TCP socket for passive mode: In this stage file contents are received on r_port and client initiates connection with server.
    '''
    print("INITIATING TRANSACTION")
        #createing a TCp socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connecting and initiating connection request to server
    client_socket.connect((server_address, r_port))

        #receiving file from server and writing it in the current directory
    #while True:
    with open(os.path.join(sys.path[0],file_received), 'wb') as f:
        print('receiving data...')
        data = client_socket.recv(1024)
        print(data)
        # write data to a file
        f.write(data)
    f.close()
    print('Successfully got the file')
    client_rcv_msg = (client_socket.recv(1024)).decode('utf-8')
    return client_rcv_msg


def main():
    '''
        Arguments:
                server_address: server ip or server name to connect to
                n_port            : server port to connect
                mode              : A (Active) or P (Passive)
                req_code          : secret integer code
                file_received : file name of file to be received from server

    '''
    try:
        server_address, mode = map(str, [sys.argv[1], sys.argv[3]])
        n_port, req_code = map(int, [sys.argv[2], sys.argv[4]])
        file_received = str(sys.argv[5])
    except IndexError:
        print("MISSING PARAMETER(S), "
              "<SERVER_ADDRESS> <N_PORT> <MODE> <REQ_CODE> <FILE_RECEIVED> REQUIRED")
        sys.exit(1)
    except ValueError:
        print("PARAMETER TYPE WRONG, TRY AGAIN")
        sys.exit(1)

    if mode == 'P':
        r_port = client_udp_negotiation_passive(server_address, n_port, req_code)
        client_rcv_msg = client_tcp_transaction_passive(server_address, r_port, file_received)
        print("CLIENT_RCV_MSG={}".format(client_rcv_msg))

    if mode == 'A':
        client_socket_a = client_udp_negotiation_active(server_address, n_port, req_code)
        client_rcv_msg = client_tcp_transaction_active(client_socket_a, file_received)
        print("CLIENT_RCV_MSG={}".format(client_rcv_msg))

if __name__ == "__main__":
    main()
