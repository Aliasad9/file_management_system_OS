import pickle
import json
import os

flat_directory = []
MAX_DIRECTORY_SIZE = 10000
class File:
    def __init__(self, filename: str, data: str):
        self.filename = filename
        self.data = data
        self.is_last = True


def create(filename, flat_directory):
    if get_file_size(flat_directory) + len(filename) >= MAX_DIRECTORY_SIZE:
        return 'Insufficient storage! Cannot create file :\'('
    if len(filename) > 32:
        return 'Unable to create file! File name cannot exceed 32 characters'
    if filename is not None and filename != '':
        file_exists = False
        for i in flat_directory:
            if i.filename != filename:
                pass
            else:
                file_exists = True
        if not file_exists:
            new_file = File(filename, '')
            flat_directory.append(new_file)
            return f'File {filename} created successfully'
        else:
            return f'Unable to create file! {filename} already exists'
    else:
        return 'Cannot create file without a name'


def convert_to_list(string_data):
    data_list = []
    buffer = ''
    for i in range(0, len(string_data)):

        if i / 32 in range(1, len(string_data)):
            buffer += string_data[i]
            data_list.append(buffer)
            buffer = ''
        else:
            buffer += string_data[i]
    if len(''.join(data_list)) < len(string_data):
        buffer = string_data[len(''.join(data_list)):len(string_data)]
        data_list.append(buffer)
    return data_list


def delete(filename, flat_directory):
    start_index = 0
    last_index = 0
    file_exists = False
    # Finding the starting index of file
    for index, i in enumerate(flat_directory):
        if i.filename == filename:
            start_index = index
            file_exists = True
            break
    if not file_exists:
        print('File not found')
        return 'File not found'
    # Finding the last index of the file
    for index, i in enumerate(flat_directory):
        if i.filename == filename and i.is_last:
            last_index = index
            break
            # Deleting the file
    del flat_directory[start_index:last_index + 1]
    return 'File deleted successfully'


def read(filename, flat_directory):
    buffer = ''
    count = 0
    # Traversing the list and appending its text in the buffer
    for i in flat_directory:
        if i.filename == filename:
            buffer += i.data
            count += 1
    if count == 0:
        print('File not found')
        return ''
    else:
        return buffer


def write(filename, data, flat_directory):
    file_exists = False
    for file_index, i in enumerate(flat_directory):

        if i.filename == filename and i.is_last:
            file_exists = True
            i.is_last = False
            if (len(data) + (len(convert_to_list(data)) * len(filename)) + get_file_size(
                    flat_directory)) > MAX_DIRECTORY_SIZE:
                return 'Insufficient storage! Cannot write to file'
            # If file is not last in the list
            if file_index + 1 != len(flat_directory):
                i.is_last = True
                files_after_required_file = []
                temporary = flat_directory
                for to_delete_index in range(file_index + 1, len(temporary)):
                    files_after_required_file.append(temporary.pop(file_index + 1))
                print(write(filename, data, temporary))
                temporary.extend(files_after_required_file)
                flat_directory = temporary
                return 'File written successfully'
            # If file is empty
            elif len(i.data) == 0:
                if len(data) <= 32:
                    f = File(filename, data)
                    flat_directory[file_index] = f
                    return 'File written successfully'
                data_list = convert_to_list(data)
                for index, files in enumerate(data_list):
                    f = File(filename, files)
                    f.is_last = False
                    if index == 0:
                        flat_directory[file_index] = f
                    elif index + 1 == len(data_list):
                        f.is_last = True
                        flat_directory.append(f)
                    else:
                        flat_directory.append(f)
                return 'File written successfully'
            # If file already has content in it
            elif len(i.data) <= 32:
                diff = 32 - len(i.data)
                i.data += data[0:diff]
                if len(data[diff:len(data)]) == 0:
                    i.is_last = True
                else:
                    i.is_last = False
                data_list = convert_to_list(data[diff:len(data)])
                for index, files in enumerate(data_list):
                    f = File(filename, files)
                    f.is_last = False
                    if index + 1 == len(data_list):
                        f.is_last = True
                    flat_directory.append(f)
                return 'File written successfully'
    if not file_exists:
        return 'File not found'


def show_memory_map(flat_directory):
    mem_map = {}
    for index, f_chunk in enumerate(flat_directory):
        if f_chunk.filename not in mem_map:
            mem_map[f_chunk.filename] = {
                'name': f_chunk.filename,
                'chunk_no.s': [index, ],
                'bytes': len(read(f_chunk.filename, flat_directory)) + len(f_chunk.filename)
            }
        else:
            chunk_list = mem_map[f_chunk.filename]['chunk_no.s']
            chunk_list.append(index)
            mem_map[f_chunk.filename] = {
                'name': f_chunk.filename,
                'chunk_no.s': chunk_list,
                'bytes': mem_map[f_chunk.filename]['bytes'] + len(f_chunk.filename)
            }
    json_formatted_str = json.dumps(mem_map, indent=4)
    print(json_formatted_str)


def read_from(filename, starting_index, size, flat_directory):
    file_data = read(filename, flat_directory)
    if len(file_data) == 0:
        print('File is empty')
    elif (starting_index + size) > len(file_data):
        print(file_data[starting_index:starting_index + size])
        print('\n\nCannot read further! ERROR: Invalid size provided.\n')
    else:
        print(file_data[starting_index:starting_index + size])


def truncate(filename, reduce_to_size, flat_directory):
    starting_index = 0
    last_index = 0
    file_exists = False
    # Finding the starting index of file
    for index, i in enumerate(flat_directory):
        if i.filename == filename:
            starting_index = index
            file_exists = True
            break
    if not file_exists:
        print('\nFile not found\n')
        return flat_directory
    # Finding the last index of the file
    for index, i in enumerate(flat_directory):
        if i.filename == filename and i.is_last:
            last_index = index
            break

    file_data = read(filename, flat_directory)
    if len(file_data) < reduce_to_size:
        print(f'\nCannot reduce size from {len(file_data)} to {reduce_to_size}\n')
        return flat_directory
    if file_exists:
        previous_chunks = flat_directory.copy()
        next_chunks = flat_directory.copy()
        del previous_chunks[starting_index:len(flat_directory)]
        del next_chunks[0:last_index + 1]
        create(filename, previous_chunks)
        print(write(filename, file_data[0:reduce_to_size], previous_chunks))
        previous_chunks.extend(next_chunks)
        return previous_chunks
    else:
        print('File not found')
        return flat_directory


def write_at(filename, write_at_index, data, flat_directory):
    starting_index = 0
    last_index = 0
    file_exists = False
    # Finding the starting index of file
    for index, i in enumerate(flat_directory):
        if i.filename == filename:
            starting_index = index
            file_exists = True
            break
    if not file_exists:
        print('\nFile not found!\n')
        return flat_directory
    # Finding the last index of the file
    for index, i in enumerate(flat_directory):
        if i.filename == filename and i.is_last:
            last_index = index
            break

    file_data = read(filename, flat_directory)
    if len(file_data) == 0:
        print('\nCannot write at index in empty file!\n')
        return flat_directory
    file_data = file_data[0:write_at_index] + data + file_data[write_at_index:len(file_data)]
    if file_exists:
        if (len(data) + (len(convert_to_list(data)) * len(filename)) + get_file_size(
                flat_directory)) > MAX_DIRECTORY_SIZE:
            print('Insufficient storage! Cannot write to file')
            return flat_directory

        previous_chunks = flat_directory.copy()
        next_chunks = flat_directory.copy()
        del previous_chunks[starting_index:len(flat_directory)]
        del next_chunks[0:last_index + 1]
        create(filename, previous_chunks)
        print(write(filename, file_data, previous_chunks))
        previous_chunks.extend(next_chunks)
        return previous_chunks
    else:
        print('\nFile not found\n')
        return flat_directory


def move_within_file(filename, from_index, to_index, size, flat_directory):
    starting_index = 0
    last_index = 0
    file_exists = False
    # Finding the starting index of file
    for index, i in enumerate(flat_directory):
        if i.filename == filename:
            starting_index = index
            file_exists = True
            break
    if not file_exists:
        print('File not found')
        return flat_directory
    # Finding the last index of the file
    for index, i in enumerate(flat_directory):
        if i.filename == filename and i.is_last:
            last_index = index
            break

    file_data = read(filename, flat_directory)
    data_to_move = file_data[from_index:from_index + size]
    if to_index > from_index and from_index + size < to_index:
        file_data = file_data[0:from_index] + file_data[from_index + size:to_index] + data_to_move + file_data[
                                                                                                     to_index:len(
                                                                                                         file_data)]
    elif from_index > to_index:
        file_data = file_data[0:to_index] + data_to_move + file_data[to_index:from_index] + file_data[
                                                                                            from_index + size:len(
                                                                                                file_data)]
    else:
        print('Unable to move data. Invalid parameters!')
        return flat_directory
    if file_exists:
        previous_chunks = flat_directory.copy()
        next_chunks = flat_directory.copy()
        del previous_chunks[starting_index:len(flat_directory)]
        del next_chunks[0:last_index + 1]
        print(create(filename, previous_chunks))
        print(write(filename, file_data, previous_chunks))
        previous_chunks.extend(next_chunks)
        print(f'\'{data_to_move}\' was moved successfully')
        return previous_chunks
    else:
        print('File not found')
        return flat_directory


def rename(filename, new_filename, flat_directory):
    file_exists = False
    new_filename_exists = False
    for f_chunk in flat_directory:
        if f_chunk.filename == new_filename:
            new_filename_exists = True
            break
    if not new_filename_exists:
        if (len(new_filename) + get_file_size(flat_directory)) > MAX_DIRECTORY_SIZE:
            return 'Insufficient storage! Cannot rename file'
        for f_chunk in flat_directory:
            if f_chunk.filename == filename:
                f_chunk.filename = new_filename
                file_exists = True
        if file_exists:
            return 'File renamed successfully'
        else:
            return f'{filename} does not exist'
    else:
        return f'Cannot rename to {new_filename}, as it already exists'


def check_file_exists(filename, flat_directory):
    file_exists = False
    for f_chunk in flat_directory:
        if f_chunk.filename == filename:
            file_exists = True
            break

    return file_exists


def serialize_data(flat_directory):
    with open('filesys.dat', 'wb') as fil:
        pickle.dump(flat_directory, fil)


def deserialize_data():
    with open('filesys.dat', 'rb') as f:
        flat_directory = pickle.load(f)
        return flat_directory


def show_help():
    print('\ncreate')
    print('delete')
    print('show_memory_map')
    print('open')
    print('rename')
    print('get_directory_size')
    print('help')
    print('exit')


def show_help_open():
    print('\nwrite')
    print('write_at')
    print('read')
    print('read_from')
    print('truncate')
    print('move')
    print('close')


def get_file_size(flat_directory):
    bytes_count = 0
    for file in flat_directory:
        bytes_count += len(file.filename)
        bytes_count += len(file.data)
    return bytes_count


def main(flat_directory):
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.path.exists('filesys.dat'):
        flat_directory = deserialize_data()
    print('**********File Management System**********\n\n')
    print('Following commands are available:')
    show_help()
    while True:
        command = str(input('\n$root./'))
        if command.strip() == 'create':
            file = str(input('Enter File name: '))
            print(create(file, flat_directory))
        elif command.strip() == 'delete':
            file = str(input('Enter File name: '))
            print(delete(file, flat_directory))
        elif command.strip() == 'show_memory_map':
            show_memory_map(flat_directory)
        elif command.strip() == 'open':
            file = str(input('Enter File name:'))
            if check_file_exists(file, flat_directory):
                show_help_open()
                while True:
                    open_command = str(input('\n$root./open/'))
                    if open_command.strip() == 'write':
                        data = str(input('Enter the text data you want to write in the file: '))
                        print(write(file, data, flat_directory))
                    elif open_command.strip() == 'write_at':
                        index = int(input('Enter the index you want to write at:'))
                        data = str(input('Enter the text data you want to write in the file: '))
                        flat_directory = write_at(file, index, data, flat_directory)
                    elif open_command.strip() == 'read':
                        data = read(file, flat_directory)
                        if len(data) == 0:
                            print('File is empty')
                        else:
                            print(data)
                    elif open_command.strip() == 'read_from':
                        starting_index = int(input('Enter the index from where to start reading: '))
                        size = int(input('Enter the size of string you want to read: '))
                        read_from(file, starting_index, size, flat_directory)
                    elif open_command.strip() == 'truncate':
                        size = int(input('Enter the size of text after being truncated: '))
                        flat_directory = truncate(file, size, flat_directory)
                    elif open_command.strip() == 'move':
                        from_index = int(input('Enter the starting index of string to move: '))
                        to_index = int(input('Enter the index where the string is to be moved: '))
                        size = int(input('Enter the size of string to move: '))
                        flat_directory = move_within_file(file, from_index, to_index, size, flat_directory)
                    elif open_command.strip() == 'help':
                        show_help_open()
                    elif open_command.strip() == 'close':
                        break
                    else:
                        print('Invalid command! Type \'help\' for more info')
            else:
                print('File does not exist')
        elif command.strip() == 'rename':
            old_name = str(input('Enter the file name: '))
            new_name = str(input('Enter the new name: '))
            print(rename(old_name, new_name, flat_directory))
        elif command.strip() == 'get_directory_size':
            print(get_file_size(flat_directory))
        elif command.strip() == 'help':
            show_help()
        elif command.strip() == 'exit':
            serialize_data(flat_directory)
            break
        else:
            print('Invalid command! Type \'help\' for more info')


main(flat_directory)
