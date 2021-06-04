import shutil
import random
import os
from PIL import Image, UnidentifiedImageError
import time
import sys
import cv2
import string
import yaml
from datetime import datetime


#Internal flags and variables.
lo = "  "
_flag = True
_rot = 0

def splitter(input_vid):
    os.chdir(in_dir)
    vidcap = cv2.VideoCapture(input_vid)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("frame%d.jpg" % count, image)
        success,image = vidcap.read()
        #print('Read a new frame #' + str(count) + ': ' + str(success))
        count += 1
        sys.stdout.write("\r" + 'Read a new frame #' + str(count) + ': ' + str(success))
        sys.stdout.flush()
    #os.remove(in_dir + input_vid)


def rotateRandom(out_path):
    i = Image.open(out_path)
    _rot = random.randint(0, 1) * 180
    print(lo + lo + "Rotating by " + str(_rot) + " degrees")
    i = i.rotate(int(_rot), expand = 1)
    i.save(out_path)
    print(lo + lo + "Rotation applied!")
    
def compensateRotation(out_path):
    i = Image.open(out_path)
    i = i.rotate(360 - int(_rot), expand = 1)
    print(lo + lo + "Compensating by " + str(360 - int(_rot)) + " degrees")
    i.save(out_path)
    print(lo + lo + "Compensation finished!")

def verifyImg(in_path, out_path):
    global _flag
    try:
        img = Image.open(out_path)
        img.verify()
        img = Image.open(out_path) 
        img.save(out_path)
        print(lo + "Verification passed!")
        _flag = False
    except (IOError, SyntaxError, OSError, UnidentifiedImageError, AttributeError, RecursionError, Image.DecompressionBombError) as e:
        shutil.copyfile(in_path, out_path)
        _flag = True
    


def glitch(out_path):
    size = os.path.getsize(out_path)
    fh = open(out_path, "r+b")
    offsets = []
    for j in range(bytes_amt):
        offset = random.randint(100, size) #offsetted to avoid corrupting the header, still breaks sometimes :(
        fh.seek(offset)      
        #offsets.append(offset)
        randomStr = ''.join(random.SystemRandom().choice(string.printable + string.digits) for _ in range(1))
        randomByteValue = bytes(randomStr, 'ASCII')
        fh.write(randomByteValue)
        #print("Edited byte @ offset: {}, [{:>5}], Value: {}".format('0x%0*X' % (5, offset), offset, '0x%0*X' % (2,ord(randomByteValue))))
        #print("New Byte Value: " + str(hex(ord(randomByteValue)).zfill(2)).upper() + ", Random Str: " + randomStr)
    fh.close()



def manager(in_path, out_path):
    global _flag
    #rotateRandom(out_path)
    _flag = True
    iterpass = 0
    while _flag:
        glitch(out_path)
        verifyImg(in_path, out_path)
        iterpass += 1
    print(lo + lo + "Working image generated in {} passes".format(iterpass))
    #compensateRotation(out_path)




def main():
    start = time.time()
    path, dirs, files = next(os.walk(in_dir))
    files_amt = 1000

    for x in range(1, files_amt + 1):
        #iterpass = 0
        _rot = random.randint(0, 3) * 90
        print("=Started Rendering frame " + str(x) +"...=")
        trailing_0 = str(x).zfill(3)
        in_path = in_dir + in_name + ext
        print(lo + "In Path: " + in_path)

        #bytes_amt = size 
        out_path = out_dir + out_name + trailing_0 + ext
        print(lo + "Out Path: " + out_path)
        shutil.copyfile(in_path, out_path)
        print(lo + "File copied!")
        manager(in_path, out_path)
        print("=Finished Rendering frame " + str(x) + ", " + str(files_amt - x) + " more to go!" + "=")
    

    
    end = time.time()
    print("=== Done! Elapsed time: " + str(end - start) + " seconds====")

    logs.close()

  


if __name__ == '__main__':
    _conf = open(r"D:\\test\\glitcher\\config.yaml", 'r')
    config = yaml.safe_load(_conf)
    print("Config Loaded!")

    in_dir      = config['in_dir']
    in_name     = config['in_name']
    ext         = config['ext']
    out_dir     = config['out_dir']
    out_name    = config['out_name']
    files_amt   = config['files_amt']
    bytes_amt   = config['bytes_amt']

    log_name = "glitch log " + datetime.now().strftime("%d-%m-%Y @ %H %M %S") + ".yaml"
    logs = open(in_dir + log_name, "w")


    print("Log created: \"{}\" ".format(in_dir + log_name))
    print("Initialised rendering...")



    main()