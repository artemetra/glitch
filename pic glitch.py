import shutil
import random
import os

in_dir = "D:\\test\\"           #input directory
in_name = "index"               #input file name
ext = ".jpeg"                   #file extension
out_dir = "D:\\test\\"          #output directory
out_name = "new"                #output file name +index
files_amt = 10                  #number of files to be outputted
#bytes_amt = 50                 #number of bytes to be modified per file

in_path = in_dir+in_name+ext
size = os.path.getsize(in_path)
bytes_amt = size 
for x in range(files_amt):
    out_path = out_dir + out_name + str(x) + ext
    shutil.copyfile(in_path, out_path)
    fh = open(out_path, "r+b")
    for j in range(bytes_amt):
        fh.seek(random.randint(100, size))
        fh.write(bytes(random.randint(0, 255)))


fh.close()
