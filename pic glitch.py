import shutil
import random
import os
from PIL import Image, UnidentifiedImageError
import time
import sys
import cv2
import string
#from numpy import rad2deg
import yaml
from datetime import datetime

#Internal flags and variables.
_flag = True
_rot = 0

def _log(text, tabbing = 0):
    print("[{}]{} {}".format(datetime.now(), "\t"*tabbing, text))
    logs.write("[{}]{} {}\n".format(datetime.now(), "\t"*tabbing, text))

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
    _log(f"Rotating by {_rot} degrees", 2)
    i = i.rotate(int(_rot), expand = 1)
    i.save(out_path)
    _log("Rotation applied!", 2)
    
def compensateRotation(out_path):
    i = Image.open(out_path)
    i = i.rotate(360 - int(_rot), expand = 1)
    _log(f"Compensating by {360 - int(_rot)} degrees", 2)
    i.save(out_path)
    _log(f"Compensation finished!", 2)

def verifyImg(in_path, out_path):
    global _flag
    try:
        img = Image.open(out_path)
        img.verify()
        img = Image.open(out_path) 
        img.save(out_path)

        _log("Verification passed!", 1)
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

        #_log("Edited byte @ offset: {}, [{:>5}], Value: {}\n".format('0x%0*X' % (5, offset), offset, '0x%0*X' % (2,ord(randomByteValue))))
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
    
    _log(f"Working image generated in {iterpass} passes", 2)
    #compensateRotation(out_path)




def main():
    start = time.time()
    #path, dirs, files = next(os.walk(in_dir))

    for x in range(1, files_amt + 1):
        #_rot = random.randint(0, 3) * 90
        
        _log(f"=Started Rendering frame {x}...=")

        trailing_0 = str(x).zfill(3)
        in_path = in_dir + in_name + ext

        _log(f"In Path: {in_path}", 1)

        #bytes_amt = size 
        out_path = out_dir + out_name + trailing_0 + ext


        _log(f"Out Path: {out_path}", 1)

        shutil.copyfile(in_path, out_path)

        _log("File copied!", 1)

        manager(in_path, out_path)

        _log(f"=Finished Rendering frame {x}, {files_amt - x} more to go!=")
    

    
    end = time.time()
    _log("=== Done! Elapsed time: {} seconds====".format(end - start))

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


    for k,v in config.items():
        print(str(k) + ": " + str(v))
    
    log_name = "glitch log " + datetime.now().strftime("%d-%m-%Y @ %H %M %S") + ".txt"
    logs = open(in_dir + log_name, "w")
    
    print("[{}] Config Loaded!\n".format(datetime.now()))
    print("[{}] Log created: \"{}\" ".format(datetime.now(), in_dir + log_name))


    print("[{}] Initialised rendering...".format(datetime.now()))



    main()