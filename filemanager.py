import tarfile
import lzma
import os
import sys
import pathlib

name = pathlib.PurePath(os.path.realpath(sys.argv[0])).name.split('.')[0] + "_files"

if(os.path.exists(name) == False):
    xz_file = lzma.LZMAFile(name, mode='w')
else:
    xz_file = lzma.LZMAFile(name, mode='a')
    
tar_xz_file = tarfile.open(mode='w', fileobj=xz_file)

def write(filename, content):
    thisfile = open(filename, "w")
    thisfile.write(content)
    thisfile.close()
    tar_xz_file.add(filename)
    os.remove(filename)
    
def read(filename):
    return tarfile.open(name,"r").extractfile(filename).read()