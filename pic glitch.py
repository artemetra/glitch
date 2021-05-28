import shutil
import random
import os
from PIL import Image, UnidentifiedImageError
import PIL
import time
import sys
import cv2
import string

in_dir = "D:\\Really Useful Files\\images\\mandel\\frames\\12_10_orig\\"           #input directory
in_name = "orig"               #input file name
ext = ".png"                   #file extension
out_dir = "C:\\test\\"          #output directory
out_name = "new"                #output file name +index
#files_amt = 10                  #number of files to be outputted
bytes_amt = 1               #number of bytes to be modified per file
#rotations = [180, 180]
lo = "  "
iterpass = 0
#offset = 2048

def glitch():
    #rotateRandom(out_path)
    fh = open(out_path, "r+b")
    offsets = []
    #iterpass += 1
    for j in range(bytes_amt):
         #offsetted to avoid corrupting the header, still breaks sometimes :(
        fh.seek(offset)      
        #offsets.append(offset)
        #bytestr = ''.join(random.SystemRandom().choice(string.printable + string.digits) for _ in range(1))
        bytestr = chr(x)
        randomByteValue = bytes(bytestr, 'UTF-8')
        fh.write(randomByteValue)
        bruhvar = randomByteValue[-1:]
        print("Edited byte @ offset: {}, [{:>5}], Value: {}, {}, {}".format('0x%0*X' % (5, offset), offset, '0x%0*X' % (2,ord(bruhvar)), randomByteValue, bruhvar))
        #print("New Byte Value: " + str(hex(ord(randomByteValue)).zfill(2)).upper() + ", Random Str: " + randomStr)
    fh.close()
    #compensateRotation(out_path)


start = time.time()
path, dirs, files = next(os.walk(in_dir))
files_amt = 512
#os.mkdir(out_dir + "0d" + str(offset) + "\\")
os.mkdir(out_dir + "halfsizeoffset" + "\\")
for x in range(0, files_amt + 1):
    
    #iterpass = 0
    rrot = random.randint(0, 3) * 90
    print("=Started Rendering frame " + str(x) +"...=")
    trailing_0 = str(x).zfill(3)
    in_path = in_dir + in_name + ext
    #print(lo + "In Path: " + in_path)
    size = os.path.getsize(in_path)
    #bytes_amt = size
    offset = size//2
    #out_path = out_dir + "0d" + str(offset) + "\\" + out_name + trailing_0 + ext
    out_path = out_dir + "halfsizeoffset" + "\\" + out_name + trailing_0 + ext
    print(lo + "Out Path: " + out_path)
    shutil.copyfile(in_path, out_path)
    print(lo + "File copied!")
    glitch()
    print("=Finished Rendering frame " + str(x) + ", " + str(files_amt - x) + " more to go!" + "=")
    
 
end = time.time()
print("=== Done! Elapsed time: " + str(end - start) + " seconds====")




