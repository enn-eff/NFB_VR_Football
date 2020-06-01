# TCP connection

TCP server socket for control of Unity scene.
While executed, saves a temporary file in the user directory with info about server address.
Server address noted in this temporary file will be read by Receiver component in Unity,
which then creates a client socket and connects to the specified address.