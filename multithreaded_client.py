import socket
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 95


def show_commands_manual():
    print('             Commands Manual\n\n')
    print('create,{}<str: filename>\n'.format(10 * ' ') +
          'delete,{}<str: filename>\n'.format(10 * ' ') +
          'rename,{}<str: old-filename>, <str: new-filename>\n'.format(10 * ' ') +
          'read,{}<str: filename>\n'.format(12 * ' ') +
          'read_from,{}<str: filename>, <int: starting-index>, <int: no._of_characters_to_read>\n'.format(7 * ' ', ) +
          'write,{}<str: filename>, <str: data-to-write>\n'.format(11 * ' ', ) +
          'write_at,{}<str: filename>, <int: to-index>, <str: data-to-write>\n'.format(8 * ' ', ) +
          'truncate,{}<str: filename>, <int: final-size-after-truncation>\n'.format(8 * ' ', ) +
          'move,{}<str: filename>, <int: from-index>, <int: to-index>, <int: size-of-string>\n'.format(12 * ' ', ) +
          'show_memory_map\n' +
          'get_directory_size\n'+'exit\n\n')


def send_my_info_to_server():
    username = str(input('Enter your name: '))
    client_socket.sendall(str.encode(username))


os.system('cls' if os.name == 'nt' else 'clear')
host = str(input('Enter the IPv4 of server: '))

print('Waiting for connection...')
try:
    client_socket.connect((host, PORT))
except socket.error as err:
    print(str(err))
    exit(0)
response = client_socket.recv(1024)
print(response.decode('utf-8'))
show_commands_manual()
send_my_info_to_server()
response = client_socket.recv(1024)
print(response.decode('utf-8'))
data = ''
while data != 'exit':
    data = input('Enter your command: ')
    client_socket.send(str.encode(data))
    response = client_socket.recv(4096)
    result = response.decode('utf-8')
    if result == 'waiting':
        print(client_socket.recv(4096).decode('utf-8'))
        print(client_socket.recv(4096).decode('utf-8'))
    else:
        print(result)
client_socket.close()
