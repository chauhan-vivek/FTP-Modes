Socket Programming
==============================
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a>
    <img src="readme-assets/intro.png" alt="Logo" width="240" height="240">
  </a>
</div>


The client will download a file from the server over the network using sockets. It uses a two-stage communication process.First stage is negotiation using UDP sockets and second stage is Transaction using TCP sockets.The requests and responses mimics the File Transfer Protocol (FTP). 

FTP runs in one of two modes; Active mode or Passive mode, which dictate the negotiation and transaction stage procedures. The following are key distinctions between the two modes:
Active Mode: random port(r_port) is attached to the TCP socket running on the client and server registers r_port internally if req_code(a secret integer shared for authorization) is verified. Also, server initiates a TCP connection with client on the client's r_port and sends the content of file.
Passive Mode: Server creates TCP socket and replies with socket's port number (r_port) after req_code is verfified. Client initiates a TCP connection to the server on servers r_port shared witg client and sends file to client.

Usage
------------
1. Clone the repo
	```
	git clone https://github.com/chauhan-vivek/UDP_Congestion_Control.git
	```
2. Create virtual environment.
	```make
	make create_environment
	```
3. Activate virtual environment.

4. Download and install all required packages.

5. Run Server
	```make
	./server.sh <REQ_CODE> 'FILE_TO_SEND'
	```

where  

REQ_CODE: is the request code which is a secret integer code that is verified when negotiating using UDP sockets. We stdout the server port in the terminal: the SERVER_PORT is the N_PORT which is to be entered in the client.sh CLI arguments in the next step.  

6. Run Client
	```make
	./client.sh <SERVER_ADDRESS> <N_PORT> <MODE> <REQ_CODE> 'file_received.txt' 
	```

where  

SERVER_ADDRESS is the address/hostname of the server to contact;  
N_PORT is the negotiation port with the server (using the earlier stdout from server);  
MODE is the mode of FTP, it can be either 'A' or 'P'  
REQ_CODE is the client request code for negotiation; and   
'file_received.txt': name of file to be saved in the current directory received from sender.  

------------