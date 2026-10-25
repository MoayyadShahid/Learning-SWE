Web sockets are used for real time communication. Creates a persistent bi-directional connection for real time communication.

HTTP uses distinct connections for each request. This adds load to the server as the server has to create a new handshake for each request. When requests are done then the connections are closed.

Web Socket is persistent as long as there is no interruptions on either side of the communication channel (no issues on client or server).

Web Sockets is a INDEPENDENT TCP-BASED protocol that is interpreted by HTTP servers to be an upgrade request.

Steps:
1. Client opens a regular HTTP GET request specifying a desired websocket URL (either prefixed with ws or wss [secure version]) with the intention to upgrade to websocket
2. Server gets the HTTP request from client and checks the headers to ensure that they are valid for websocket upgrade. If all is good server returns 101 (switching protocols) to indicate successful upgrade to websocket
3. Now client and server can communicate over websockets via the established TCP connection, HTTP connection is replaced by websocket connection  
4. Some points of failure on server end, if sec-websocket-accept value in server does not match the expected value, or if there are headers missing or if the server returns anything other than 101 response then the connection will not be established

- Default port 80 is used for ws
- Default port 443 is used for wss

WSS is used as a secure URI as TLS handshake is done between client and server for secure communication 

Data is transmitted via a sequence of 'frames' between client and server in websockets. Frames are the basic units in WS. 

Frames have a specific structure:
FIN : 0 / 1 [1 is indicating the final frame]
RSV 1,2,3: 3 reserve bits stored for future use
opcode: 4 bits to indicate whether utf-8 text data, binary, health ping, etc. is sent
Payload length: 7 bits
Masking Key: 32 bits
Payload Data: variable size

Masking basically helps ensure that the request doesn't seem like an HTTP request, making WS requests look different

Fragments: splitting a large message into smaller chunks, done to prevent buffer overflow
