import sys
from socketIO_client import SocketIO, LoggingNamespace

print "\n".join(sys.argv)

with SocketIO('localhost', 3333) as socketIO:
    socketIO.emit('bbb')
    socketIO.wait_for_callbacks(seconds=1)
