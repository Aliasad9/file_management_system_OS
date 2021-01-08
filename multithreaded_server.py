import socket

from lab import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 95
thread_count = 0
flat_directory = []

try:
    server_socket.bind((host, port))

except socket.error as err:
    print(str(err))
print('Waiting for connection...')
server_socket.listen(5)

threads = []
if os.path.exists('filesys.dat'):
    flat_directory = deserialize_data()


def convert_text_to_command(line):
    commands = line.split(", ")
    com = Command()
    for index, i in enumerate(commands):
        if index == 0:
            com.name = i
        elif index == 1:
            com.filename = i
        else:
            i = i.strip('\n')
            com.args.append(i)
    return com


def client_thread(connection, thread_no):
    global flat_directory
    connection.sendall(str.encode("\n**********File Management Server**********\n\n"))
    username = connection.recv(1024).decode('utf-8')
    welcome_msg = 'Hello, {}'.format(username)
    connection.sendall(str.encode(welcome_msg))

    while True:
        data = connection.recv(1024)
        reply = data.decode('utf-8')
        command = convert_text_to_command(reply)
        if not data:
            break
        if reply == 'exit':
            print(f'Client: {thread_no}\'s socket closed')
            serialize_data(flat_directory)
            break
        flat_directory = thread_function([command], connection, flat_directory)
        # connection.sendall(str.encode(reply))

    connection.close()


while True:
    client, address = server_socket.accept()
    print('Connected to ' + address[0] + ":" + str(address[1]))
    thread = CustomThread(target=client_thread, args=(client, thread_count))
    threads.append(thread)
    thread.start()

    thread_count += 1
    print('thread number: ' + str(thread_count))
