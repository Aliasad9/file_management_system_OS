# File Management System

It provides all the functions that are required to manage files in an OS. <br> Following commands are allowed:
- create, \<str: filename\>
- delete, \<str: filename\>
- rename, \<str: old-filename\>, \<str: new-filename\>
- read, \<str: filename\>
- read_from, \<str: filename\>, \<int: starting-index\>, \<int: no._of_characters_to_read\>
- write, \<str: filename\>, \<str: data-to-write\>
- write_at, \<str: filename\>, \<int: to-index\>, \<str: data-to-write\>
- truncate, \<str: filename\>, \<int: final-size-after-truncation\>
- move, \<str: filename\>, \<int: from-index\>, \<int: to-index\>, \<int: size-of-string\>
- show_memory_map
- get_directory_size

## Instructions

1. Check the ip of the the your own device by typing the following command in terminal/command prompt.
> ipconfig
2. Just open the terminal in the root directory, and run the server code: 
> python multithreaded_server.py
3. Then run the client code on a device on the same network by the following command:
> python multithreaded_client.py
4. Enter the IP of the server device when prompted for.
5. All the available commands manual will be displayed when connection with server is established.
6. Enter your name and a response will be received from server.
7. And then keep entering your commands according to the manual or exit if you are done using the program.
