import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tqdm import tqdm

import time
import shutil
import os
import cv2
from glob import glob as gg


save_folder_path = None
folder_path = None


def get_paths(path):

    if os.path.isdir(path):
        path += '\*'
        path = path.replace('\\', '/')

    files = gg(path)
    path_list += files

    for file in files:
        if os.path.isdir(file):
            get_paths(path_list, file)


def do_copy():
    for path in path_list:
        try:
            shutil.copy(path, save_folder_path)
        except PermissionError as e:
            print(f"Error: {e}")


def start():
    while True:
        get_paths(folder_path)
        do_copy()
        time.sleep(time_period)


tk_title = "Cut Video"

root=tk.Tk()
root.title(tk_title)
root.geometry("500x240+560+400")


path_list = []
time_period = 10


def choose_save_path():
    save_folder_path = filedialog.askdirectory()
    update_save_path_label_text(save_folder_path)

def choose_folder():
    folder_path = filedialog.askdirectory()
    update_folder_label_text(folder_path)


def update_save_path_label_text(save_folder_path):
    save_path_label.config(text=f"New Folder Path: {save_folder_path}")

def update_folder_label_text(folder_path):
    folder_label.config(text=f"New Folder Path: {folder_path}")


folder_label = tk.Label(root, text="Choose a folder File to Cut:")
folder_label.pack()


save_path_label = tk.Label(root, text="Choose save Folder to Store")
save_path_label.pack()


choose_folder_button = tk.Button(root, text="Choose folder", command=choose_folder)
choose_folder_button.pack()


choose_save_path_button = tk.Button(root, text="Choose Save Folder", command=choose_save_path)
choose_save_path_button.pack()


start_button = tk.Button(root, text="Start", command=start)
start_button.pack()

root.mainloop()