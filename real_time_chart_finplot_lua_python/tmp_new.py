import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8888))
s.listen(5)
while True:
    print('Цикл')
    try:
        print('try:')
        client, addr = s.accept()
        print(f'{client=}, {addr=}')
    except KeyboardInterrupt:
        print('Close')
        s.close()
        break
    else:
        print('else')
        result = client.recv(1024)
        print('Message:', result.decode('utf-8'))
