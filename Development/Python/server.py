#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#


from Python.EEG import EEG
import time
import zmq

#region
#   Class EEG instantiated and  
#   Get the data stream and send it to unity continuously
if __name__ == "__main__":
    eegObject = EEG.__init__(self=EEG)
#endregion

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)

        #  Do some 'work'.
        #  Try reducing sleep time to 0.01 to see how blazingly fast it communicates
        #  In the real world usage, you just need to replace time.sleep() with
        #  whatever work you want python to do, maybe a machine learning task?
        time.sleep(0.01)

        #  Send reply back to client
        #  In the real world usage, after you finish your work, send your output here
        socket.send(eegObject)

