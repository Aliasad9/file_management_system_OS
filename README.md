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
1. Write the commands you want to be executed in files named "input_threads_\<x\>.txt" in the working directory.(where x is the thread number)
2. Open command prompt in the folder and run 
> python lab.py
3. Provide the number of threads you want to run when prompted. (Make sure you have the same number of input_threads_\<x\>.txt in the same directory)
4. And DONE.<br>
You will see x number of output_threads_\<x\>.txt files generated with respective outputs generated in threads
