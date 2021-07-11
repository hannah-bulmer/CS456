# README

Author: Hannah Bulmer

Student ID: 20714790

This client-server program allows client to send messages to server and have them returned reversed. The server must be running before the client can send it messages. Clients can send messages as long as the server remains open, however there is no compatibility for multiple clients sending messages at the same time.

## Instructions

In order to run the server and client, you must have `python3` installed. To ensure this, you can run `which python3` or `python3 -V`. To install python3 on Mac, you can install Homebrew and run `brew install python`. 

***

On server machine, launch the server by running 
```
./server.sh <req_num>
```
where `req_num` can be any int value. The same `req_num` has to be provided to both client and server.

***

On client machine, launch client by running
```
./client.sh <server_addr> <n_port> <req_code> <msg>
```

`server_addr` is the IP address or hostname of the machine currently running the server (e.g. `ubuntu2004-004`). `<n_port>` is the port num the server is running on - it will be printed out by the server when it is launched. `<req_code>` needs to match the server's `<req_code>` in order to successfully communication msgs. `<msg>` is the string you would like to have reversed.
