import shutil
import random
import os
from PIL import Image, UnidentifiedImageError
import time
import sys
import cv2
import string
from numpy import rad2deg
import yaml
from datetime import datetime


#Internal flags and variables.
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
    print("[{}] \t\tRotating by {} degrees".format(datetime.now(), _rot))
    i = i.rotate(int(_rot), expand = 1)
    i.save(out_path)
    print("[{}] \t\tRotation applied!".format(datetime.now()))
    
def compensateRotation(out_path):
    i = Image.open(out_path)
    i = i.rotate(360 - int(_rot), expand = 1)
    print("[{}] \t\tCompensating by {} degrees".format(datetime.now(), 360 - int(_rot)))
    i.save(out_path)
    print("[{}] \t\tCompensation finished!".format(datetime.now()))

def verifyImg(in_path, out_path):
    global _flag
    try:
        img = Image.open(out_path)
        img.verify()
        img = Image.open(out_path) 
        img.save(out_path)

        print(      "[{}] \tVerification passed!".format(datetime.now()))
        logs.write( "[{}] \tVerification passed!\n".format(datetime.now()))
        _flag = False
    except (IOError, SyntaxError, OSError, UnidentifiedImageError, AttributeError, RecursionError, Image.DecompressionBombError) as e:
        shutil.copyfile(in_path, out_path)
        _flag = True
    


def glitch(out_path):
    size = os.path.getsize(out_path)
    fh = open(out_path, "r+b")
    offsets = []
    for _ in range(bytes_amt):
        offset = random.randint(200, size) #offsetted to avoid corrupting the header, still breaks sometimes :(
        fh.seek(offset)      
        offsets.append(offset)
        randomStr = ''.join(random.SystemRandom().choice(string.printable + string.digits) for _ in range(1))
        randomByteValue = bytes(randomStr, 'ASCII')
        fh.write(randomByteValue)

        logs.write("[{}] Edited byte @ offset: {}, [{:>5}], Value: {}\n".format(datetime.now(),'0x%0*X' % (5, offset), offset, '0x%0*X' % (2,ord(randomByteValue))))
        #logs.write("[{}] New Byte Value: {}\n".format(datetime.now(), str(hex(ord(randomByteValue)).zfill(2)).upper()))
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
    
    print(      "[{}] \t\tWorking image generated in {} passes".format(datetime.now(), iterpass))
    logs.write( "[{}] \t\tWorking image generated in {} passes\n".format(datetime.now(), iterpass))
    #compensateRotation(out_path)




def main():
    start = time.time()
    #path, dirs, files = next(os.walk(in_dir))

    for x in range(1, files_amt + 1):
        #_rot = random.randint(0, 3) * 90
        
        print(      "[{}] =Started Rendering frame {}...=".format(datetime.now(), x))
        logs.write( "[{}] =Started Rendering frame {}...=\n".format(datetime.now(), x))

        trailing_0 = str(x).zfill(3)
        in_path = in_dir + in_name + ext

        print(      "[{}] \tIn Path: {}".format(datetime.now(), in_path))
        logs.write( "[{}] \tIn Path: {}\n".format(datetime.now(), in_path))

        #bytes_amt = size 
        out_path = out_dir + out_name + trailing_0 + ext

        print(      "[{}] \tOut Path: {}".format(datetime.now(), out_path))
        logs.write( "[{}] \tOut Path: {}\n".format(datetime.now(), out_path))

        shutil.copyfile(in_path, out_path)

        print(      "[{}] \tFile copied!".format(datetime.now()))
        logs.write( "[{}] \tFile copied!\n".format(datetime.now()))

        manager(in_path, out_path)

        print(      "[{}] =Finished Rendering frame {}, {} more to go!=".format(datetime.now(), x, files_amt - x))
        logs.write( "[{}] =Finished Rendering frame {}, {} more to go!=\n".format(datetime.now(), x, files_amt - x))
    

    
    end = time.time()
    print(      "[{}] === Done! Elapsed time: {} seconds====".format(datetime.now(), end - start))
    logs.write( "[{}] === Done! Elapsed time: {} seconds====\n".format(datetime.now(), end - start))

    logs.close()

  


if __name__ == '__main__':
    _conf = open(r"D:\\test\\glitcher\\config.yaml", 'r')
    config = yaml.safe_load(_conf)

    in_dir      = config['in_dir']
    in_name     = config['in_name']
    ext         = config['ext']
    out_dir     = config['out_dir']
    out_name    = config['out_name']
    files_amt   = config['files_amt']
    bytes_amt   = config['bytes_amt']

    log_name = "glitch log " + datetime.now().strftime("%d-%m-%Y @ %H %M %S") + ".txt"
    logs = open(in_dir + log_name, "w")

    for k,v in config.items():
        print(str(k) + ": " + str(v))
    
    log_name = "glitch log " + datetime.now().strftime("%d-%m-%Y @ %H %M %S") + ".txt"
    logs = open(in_dir + log_name, "w")
    print("[{}] Config Loaded!\n".format(datetime.now()))
    print("[{}] Log created: \"{}\" ".format(datetime.now(), in_dir + log_name))

    print("[{}] Initialised rendering...".format(datetime.now()))



    main()