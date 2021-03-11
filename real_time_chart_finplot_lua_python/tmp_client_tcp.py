import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 3599))

s.send(b'Test message. Test message. Test message. Test message. Test message.\n')

s.send(b'Long string. Long string. Long string. Long string. Long string. Long string. '
       b'Long string. Long string. Long string. Long string. Long string. Long string. '
       b'Long string. Long string. Long string. Long string. Long string. Long string. '
       b'Long string. Long string. Long string. Long string. Long string. Long string. '
       b'Long string. Long string. Long string. Long string. Long string. Long string. '
       b'Long string. Long string. Long string. Long string. Long string. Long string. '
       b'Long string. Long string. Long string. Long string. Long string. Long string. \n')

s.send(b'New string. New string. New string. New string. New string. New string.\n')

s.close()
