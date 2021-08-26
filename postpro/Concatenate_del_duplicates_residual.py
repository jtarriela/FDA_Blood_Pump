import glob
import os
import shutil
import hashlib

# print(glob.glob(r"/Users/jdtarriela/Desktop/C5_Residuals/0-6400/*.out"))
dir_list = [r'/Users/jdtarriela/Desktop/C5_Residuals/0-6400/',
            r'/Users/jdtarriela/Desktop/C5_Residuals/6400-8000/',
            r'/Users/jdtarriela/Desktop/C5_Residuals/15000-22800/',
            r'/Users/jdtarriela/Desktop/C5_Residuals/22800-24000/']

#todo: get files to use
#file_list = glob.glob(r"/Users/jdtarriela/Desktop/C5_Residuals/0-6400/*.out")
filenames = [os.path.basename(x) for x in glob.glob(r"/Users/jdtarriela/Desktop/C5_Residuals/0-6400/*.out")]

#todo: append files by searching eahc folder save to ~/appended
for file in filenames:
    # Reset Directory list to be appended for every file
    dir_list = [r'/Users/jdtarriela/Desktop/C5_Residuals/0-6400/',
                r'/Users/jdtarriela/Desktop/C5_Residuals/6400-8000/',
                r'/Users/jdtarriela/Desktop/C5_Residuals/15000-22800/',
                r'/Users/jdtarriela/Desktop/C5_Residuals/22800-24000/']
    # Append directories with file name
    for i in enumerate(dir_list):
        root = dir_list[i[0]]
        dir_list[i[0]] = root + file
        print(dir_list[i[0]])
        # print(i)

    # Concatenate text files together and save out to new folder
    output_path = r'/Users/jdtarriela/Desktop/C5_Residuals/appended/' + file
    with open(output_path, 'wb') as wfd:
        for f in dir_list:
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

#todo: remove duplicates for i in filenames
#todo: fix overwriting leaving empty files
path_input = r'/Users/jdtarriela/Desktop/C5_Residuals/appended/'
path_output = r'/Users/jdtarriela/Desktop/C5_Residuals/del_duplicates/'
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


