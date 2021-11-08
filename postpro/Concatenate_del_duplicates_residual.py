import glob
import os
import shutil
import hashlib

# todo: get files to use
filenames = [os.path.basename(x) for x in glob.glob(r"/Users/jdtarriela/Desktop/KW/C5/3240-3600/*.out")]

dir_list_1 = [r'/Users/jdtarriela/Desktop/KW/C5/3240-3600/',
              r'/Users/jdtarriela/Desktop/KW/C5/720-3240/',
              r'/Users/jdtarriela/Desktop/KW/C5/0-720/']

path_input = r'/Users/jdtarriela/Desktop/KW/C5/temp_files/'
path_output = r'/Users/jdtarriela/Desktop/KW/C5/Final_residuals/'

# Check whether the
# specified path is
# an existing file
IO_path = [path_input, path_output]
for i in IO_path:
    isFile = os.path.isfile(i)
    if isFile == True:
        print('Path {} exists'.format(i))
        print('Script Break, remove temp folder')
        break
    else:
        print('Path {} does not exist'.format(i))
        os.mkdir(i)
        print('Path {} created \n'.format(i))

#todo: append files by searching eahc folder save to ~/appended
for file in filenames:
    # Reset Directory list to be appended for every file
    # Function doesnt like when dir_list outside for list

    # dir_list = [r'/Users/jdtarriela/Desktop/C5_Residuals/0-6400/',
    #             r'/Users/jdtarriela/Desktop/C5_Residuals/6400-8000/',
    #             r'/Users/jdtarriela/Desktop/C5_Residuals/15000-22800/',
    #             r'/Users/jdtarriela/Desktop/C5_Residuals/22800-24000/']

    dir_list = dir_list_1[:] # [:] copy explicity without reference
    # Append directories with file name
    for i in enumerate(dir_list):
        root = dir_list[i[0]]
        dir_list[i[0]] = root + file
        print(dir_list[i[0]])
        # print(i)

    # Concatenate text files together and save out to new folder
    output_path = path_input + file
    with open(output_path, 'wb') as wfd:
        for f in dir_list:
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

#todo: remove duplicates for i in filenames
#todo: fix overwriting leaving empty files
for file in filenames:
    print(file)
    print(path_output)
    #1
    input_file_path = path_input + file
    output_file_path = path_output + file
    #2
    completed_lines_hash = set()
    #3
    output_file = open(output_file_path, "w")
    #4
    for line in open(input_file_path, "r"):
        #5
        hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
        #6
        if hashValue not in completed_lines_hash:
            output_file.write(line)
            completed_lines_hash.add(hashValue)

    #7
    output_file.close()

    # Delete first and third lines
    with open(output_file_path, "r") as infile:
        lines = infile.readlines()

    with open(output_file_path, "w") as outfile:
        for pos, line in enumerate(lines):
            if pos != 0 and pos != 2:
                outfile.write(line)

shutil.rmtree(path_input, ignore_errors = False)
