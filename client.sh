#!/bin/bash

#Run script for client distributed as part of 
#Assignment 1
#Computer Networks (CS 456)
#Number of parameters: 5
#Parameter:
#    $1: <server_address>
#    $2: <n_port>
#    $3: <mode>
#    $4: <req_code>
#    $5: <file_received>

#Uncomment/update exactly one of the following commands depending on your implementation

#For C/C++ implementation
#./client $1 $2 "$3" $4 "$5"

#For Java implementation
#java client $1 $2 "$3" $4 "$5"

#For Python implementation
python client.py $1 $2 "$3" $4 "$5"

#For Ruby implementation
#ruby client.rb $1 $2 "$3" $4 "$5"