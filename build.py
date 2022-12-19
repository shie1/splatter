from platform import system as os
from os import system as exec
from glob import glob
from os import chdir, path, getcwd, mkdir, remove
import platform
from shutil import rmtree
from sys import argv


def data(file, alias=""):
    if(alias == ""):
        alias = file
    if(os() == "Windows"):
        d = ";"
    else:
        d = ":"
    return f'--add-data "{file}{d}{file}"'


def hiddenimport(module):
    return f'--hidden-import {module}'


if(len(argv) > 1):
    name = argv[1].replace('.py', '')
else:
    name = path.split(getcwd())[-1]

imports = []

try:
    for module in open("requirements.txt", "r").read().split("\n"):
        imports.append(module.split("==")[0])
except:
    ""

install = f'pyinstaller -y --distpath "dist" --name "{name}"'

for file in glob("*.py"):
    if(file == ""):
        continue
    install += f" {data(file)}"
    imports.append(file)

for module in imports:
    if(module == ""):
        continue
    install += f" {hiddenimport(module)}"

if(len(argv) > 1):
    src = argv[1]
elif(path.exists("main.py") == False):
    src = glob("*.py")[0]
else:
    src = "main.py"

install += f" -F {src}"

print(install)
exec(install)

try:
    remove(name + '.spec')
except:
    ""
try:
    rmtree('__pycache__')
except:
    ""
try:
    rmtree('build')
except:
    ""
