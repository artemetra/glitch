import shutil
import random
import os
from PIL import Image, UnidentifiedImageError
import PIL
import time
import sys
import cv2
import string

in_dir = "D:\\Really Useful Files\\images\\mandel\\frames\\12_8_orig\\"           #input directory
in_name = "new"               #input file name
ext = ".jpg"                   #file extension
out_dir = "D:\\Really Useful Files\\images\\mandel\\frames\\12_8\\"          #output directory
out_name = "new000"                #output file name +index
#files_amt = 10                  #number of files to be outputted
bytes_amt = 2               #number of bytes to be modified per file
#rotations = [180, 180]
lo = "  "

def splitter(input_vid):
    os.chdir(in_dir)
    vidcap = cv2.VideoCapture(input_vid)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        #print('Read a new frame #' + str(count) + ': ' + str(success))
        count += 1
        sys.stdout.write("\r" + 'Read a new frame #' + str(count) + ': ' + str(success))
        sys.stdout.flush()
    #os.remove(in_dir + input_vid)


def rotateRandom(out_path):
    i = Image.open(out_path)
    #rrot = random.randint(0, 1) * 180
    print(lo + lo + "Rotating by " + str(rrot) + " degrees")
    i = i.rotate(int(rrot), expand = 1)
    i.save(out_path)
    print(lo + lo + "Rotation applied!")
    
def compensateRotation(out_path):
    i = Image.open(out_path)
    i = i.rotate(360 - int(rrot), expand = 1)
    print(lo + lo + "Compensating by " + str(360 - int(rrot)) + " degrees")
    i.save(out_path)
    print(lo + lo + "Compensation finished!")

def verifyImg(in_path, out_path):
    try:
        img = Image.open(out_path) 
        img.verify() 
        img.save(out_path)
        print(lo + "Verification passed!")
    except (IOError, SyntaxError, OSError, UnidentifiedImageError, AttributeError) as e:
        print(lo + "Bad image, error: " + str(e) + ", retrying glitch...")
        os.remove(out_path)
        print(lo + "File deleted!")
        shutil.copyfile(in_path, out_path)
        print(lo + "File replaced!")
        glitch()

def glitch():
    rotateRandom(out_path)
    fh = open(out_path, "r+b")
    for j in range(bytes_amt):
        offset = random.randint(100, size) #offsetted to avoid corrupting the header, still breaks sometimes :(
        fh.seek(offset)      
        #print(lo + lo + "Byte offset: " + str(offset))
        randomStrTest = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(1))
        print(lo + lo + "Random Str: " + randomStrTest)
        randomByteValue = bytes(random.randint(0, 255))
        fh.write(randomByteValue)
        #print("New Byte Value: " + str(randomByteValue))
    #verifyImg(in_path, out_path)
    compensateRotation(out_path)
    fh.close()

start = time.time()
path, dirs, files = next(os.walk(in_dir))
files_amt = 40
for x in range(1, files_amt + 1):
    rrot = random.randint(0, 3) * 90
    print("=Started Rendering frame " + str(x) +"...=")
    trailing_0 = str(x).zfill(3)
    in_path = in_dir + in_name + ext
    print(lo + "In Path: " + in_path)
    size = os.path.getsize(in_path)
    #bytes_amt = size 
    out_path = out_dir + out_name + trailing_0 + ext
    print(lo + "Out Path: " + out_path)
    shutil.copyfile(in_path, out_path)
    print(lo + "File copied!")
    glitch()
    print("=Finished Rendering frame " + str(x) + ", " + str(files_amt - x) + " more to go!" + "=")
 
end = time.time()
print("=== Done! Elapsed time: " + str(end - start) + " seconds====")


