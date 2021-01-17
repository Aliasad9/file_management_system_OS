import socket
import os
from lab import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 95
thread_count = 1
flat_directory = []
all_connected_users = []
readers_list = []
writers_list = []

event = Event()


class User:
    def __init__(self, addr, name, connection):
        self.addr = addr
        self.name = name
        self.connection = connection


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
    print("{:>16} {:>16} {:>16}".format("User", "IP Address", "Port Number"))

    for index, user in enumerate(all_connected_users):
        print("{:>16} {:>16} {:>16}".format(user.name, user.addr[0], user.addr[1]))


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


def thread_function(commands, conn, flat_directory):
    for i in commands:
        if i.name.strip('\n') == 'show_memory_map' and i.filename is None and len(i.args) == 0:
            count = 0
            while len(writers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                readers_list.append(conn)
                show_memory_map(flat_directory, conn)
            except:
                conn.sendall(str.encode('Invalid arguments!\n Try:\n\t show_memory_map'))
            readers_list.remove(conn)
        elif i.name == 'read' and i.filename is not None and i.filename != '' and len(i.args) == 0:
            count = 0
            while len(writers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                readers_list.append(conn)

                data = read(i.filename.strip('\n'), flat_directory, conn)
                if len(data) == 0:
                    conn.sendall(str.encode('File is empty'))
                else:
                    conn.sendall(str.encode(data))
            except:
                conn.sendall(str.encode('Invalid arguments!\n Try:\n\tread, <string: filename>'))
            readers_list.remove(conn)

        elif i.name == 'read_from' and i.filename is not None and i.filename != '' and len(i.args) > 0:
            count = 0
            while len(writers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                readers_list.append(conn)
                starting_index = int(i.args[0])
                size = int(i.args[1])
                read_from(i.filename.strip('\n'), starting_index, size, flat_directory, conn)
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\tread_from, <string: filename>, ' +
                        '<int: starting-index>, <int: size>'
                    )
                )
            readers_list.remove(conn)

        elif i.name == 'write' and i.filename is not None and i.filename != '' and len(i.args) > 0:

            count = 0

            while len(readers_list) > 0 or len(writers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                writers_list.append(conn)
                threadLock.acquire()
                event.wait(10)
                data = str(i.args[0].strip("\""))
                conn.sendall(str.encode(write(i.filename.strip('\n'), data, flat_directory)))
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\tcreate, <string: filename>, "<string: text-data">'
                    )
                )
            writers_list.remove(conn)
            threadLock.release()

        elif i.name == 'write_at' and i.filename is not None and i.filename != '' and len(i.args) > 0:

            count = 0

            while len(readers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                writers_list.append(conn)
                threadLock.acquire()
                index = int(i.args[0])
                data = str(i.args[1].strip("\""))
                flat_directory = write_at(i.filename, index, data, flat_directory, conn)
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\twrite_at, <string: filename>, ' +
                        '<int: to-index>, "<string: text-data>"'
                    )
                )
            writers_list.remove(conn)
            threadLock.release()

        elif i.name == 'truncate' and i.filename is not None and i.filename != '' and len(i.args) > 0:

            count = 0

            while len(readers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                writers_list.append(conn)
                threadLock.acquire()
                size = int(i.args[0])
                flat_directory = truncate(i.filename, size, flat_directory, conn)
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\ttruncate, <string: filename>,' +
                        ' <int: final-size-after-truncation>'
                    )
                )
            writers_list.remove(conn)
            threadLock.release()
        elif i.name == 'move' and i.filename is not None and i.filename != '' and len(i.args) > 0:

            count = 0

            while len(readers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                writers_list.append(conn)
                threadLock.acquire()
                from_index = int(i.args[0])
                to_index = int(i.args[1])
                size = int(i.args[2])
                flat_directory = move_within_file(i.filename, from_index, to_index, size, flat_directory, conn)
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\tmove, <string: filename>, ' +
                        '<int: from-index>, <int: to-index>, <int: size-of-string>'
                    )
                )
            writers_list.remove(conn)
            threadLock.release()
        elif i.name == 'delete' and i.filename is not None and i.filename != '' and len(i.args) == 0:

            count = 0

            while len(readers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                writers_list.append(conn)
                threadLock.acquire()
                file = str(i.filename.strip("\n"))
                conn.sendall(str.encode(delete(file, flat_directory)))
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\tdelete, <string: filename>'
                    )
                )
            writers_list.remove(conn)
            threadLock.release()
        elif i.name == 'create' and i.filename is not None and i.filename != '' and len(i.args) == 0:

            count = 0

            while len(readers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                writers_list.append(conn)
                threadLock.acquire()
                file = str(i.filename.strip("\n"))
                conn.sendall(str.encode(create(file, flat_directory)))
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\tcreate, <string: filename>'
                    )
                )
            writers_list.remove(conn)
            threadLock.release()
        elif i.name == 'rename' and i.filename is not None and i.filename != '' and len(i.args) > 0:

            count = 0

            while len(readers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                writers_list.append(conn)
                threadLock.acquire()
                old_name = str(i.filename.strip('\n'))
                new_name = str(i.args[0])
                conn.sendall(str.encode(rename(old_name, new_name, flat_directory)))
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\trename, <string: old-filename>,' +
                        ' <string: new-filename>'
                    )
                )
            writers_list.remove(conn)
            threadLock.release()
        elif i.name == 'get_directory_size' and i.filename is None and len(i.args) == 0:
            count = 0
            while len(writers_list) > 0:
                if count == 0:
                    conn.sendall(str.encode('waiting'))
                    conn.sendall(str.encode("Cannot access file at the moment...."))
                count += 1

            try:
                readers_list.append(conn)
                conn.sendall(str.encode(str(get_file_size(flat_directory))))
            except:
                conn.sendall(
                    str.encode(
                        'Invalid arguments!\n Try:\n\tget_directory_size'
                    )
                )
            readers_list.remove(conn)
        else:
            conn.sendall(str.encode(f'Invalid arguments: {i.name}, {i.filename}, {i.args}'))

    return flat_directory


def client_thread(connection, addr):
    global flat_directory
    connection.sendall(str.encode("\n**********File Management Server**********\n\n"))
    username = connection.recv(1024).decode('utf-8')
    user = User(addr, username, connection)
    all_connected_users.append(user)
    display_current_active_users()
    welcome_msg = 'Hello, {}'.format(username)
    connection.sendall(str.encode(welcome_msg))

    while True:
        data = connection.recv(4096)
        reply = data.decode('utf-8')
        command = convert_text_to_command(reply)

        if not data:
            break
        if reply == 'exit':
            all_connected_users.remove(user)
            display_current_active_users()
            print(f'\n\n{user.name}\'s thread closed for connection: {addr[0]}:{addr[1]}')
            serialize_data(flat_directory)
            break
        flat_directory = thread_function([command], connection, flat_directory)

    connection.close()


while True:
    client, address = server_socket.accept()
    thread = CustomThread(target=client_thread, args=(client, address))
    threads.append(thread)
    thread.start()
    thread_count += 1
