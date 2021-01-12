import socket

from lab import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 95
thread_count = 1
flat_directory = []
all_connected_users = []

try:
    server_socket.bind((host, port))

except socket.error as err:
    print(str(err))
print('Waiting for connection...')
server_socket.listen(5)

threads = []
if os.path.exists('filesys.dat'):
    flat_directory = deserialize_data()


def display_current_active_users():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("*************** Current Active Users ***************")
    print("{:>16} {:>16} {:>16}".format("User number", "IP Address", "Port Number"))

    for index, addr in enumerate(all_connected_users):
        print("{:>16} {:>16} {:>16}".format(index + 1, addr[0], addr[1]))


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


def client_thread(connection, addr):
    global flat_directory
    connection.sendall(str.encode("\n**********File Management Server**********\n\n"))
    username = connection.recv(1024).decode('utf-8')
    welcome_msg = 'Hello, {}'.format(username)
    connection.sendall(str.encode(welcome_msg))

    while True:
        data = connection.recv(4096)
        reply = data.decode('utf-8')
        command = convert_text_to_command(reply)
        if not data:
            break
        if reply == 'exit':
            all_connected_users.remove(addr)
            display_current_active_users()
            print(f'\n\nThread closed for connection: {addr[0]}:{addr[1]}')
            serialize_data(flat_directory)
            break
        flat_directory = thread_function([command], connection, flat_directory)
    connection.close()


while True:
    client, address = server_socket.accept()
    all_connected_users.append(address)
    display_current_active_users()
    thread = CustomThread(target=client_thread, args=(client, address))
    threads.append(thread)
    thread.start()
    thread_count += 1
