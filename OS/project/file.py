import os
import time
from glob import glob as gg
import shutil


DEAFAULT_FOLDER = os.getcwd()
destination = r"C:\Users\Elara\Downloads\reserve"


def get_paths(path_list, path):

    if os.path.isdir(path):
        path += '\*'
        path = path.replace('\\', '/')

    files = gg(path)
    path_list += files

    for file in files:
        if os.path.isdir(file):
            get_paths(path_list, file)
            

def do_copy(path_list):

    for path in path_list:
        try:
            shutil.copy(path, destination)
        except PermissionError as e:
            print(f"Error: {e}")


path_list = []

time_period = 3600


while True:
    get_paths(path_list, DEAFAULT_FOLDER)
    do_copy(path_list)
    time.sleep(time_period)
