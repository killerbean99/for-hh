from tkinter import *
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tqdm import tqdm
import cv2
from ctypes import windll

# Define the colors for the dark theme
BG_COLOR = "#1C1C1C"
FG_COLOR = "#F8F8FF"
BUTTON_BG_COLOR = "#4A4A4A"
BUTTON_FG_COLOR = "#F8F8FF"
PROGRESS_COLOR = "#00BFFF"
DEAFAULT_FOLDER = os.getcwd()
save_folder_path = None

#this code works fine on windows 10, i didn't try it in any other OS, if you use window 8, 7, ... 
#or you use a distro of linux, you can try it anyway
#this code works fine as a exe made in pyinstaller

tk_title = "Cut Video" # Put here your window title

root=tk.Tk() # root (your app doesn't go in root, it goes in window)
root.title(tk_title) 
root.overrideredirect(True) # turns off title bar, geometry
root.geometry('800x300+560+390') # set new geometry the + 75 + 75 is where it starts on the screen
#root.iconbitmap("your_icon.ico") # to show your own icon 
root.minimized = False # only to know if root is minimized
root.maximized = False # only to know if root is maximized

LGRAY = '#3e4042' # button color effects in the title bar (Hex color)
DGRAY = '#25292e' # window background color               (Hex color)
RGRAY = '#10121f' # title bar color                       (Hex color)

root.config(bg=BG_COLOR)
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)


def set_appwindow(mainWindow): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True
    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())
    

def minimize_me():
    root.attributes("-alpha",0) # so you can't see the window when is minimized
    root.minimized = True       


def deminimize(event):
    root.focus() 
    root.attributes("-alpha",1) # so you can see the window when is not minimized
    if root.minimized == True:
        root.minimized = False                              
        

def maximize_me():
    if root.maximized == False: # if the window was not maximized
        root.normal_size = root.geometry()
        expand_button.config(text=" 🗗 ")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.maximized = not root.maximized 
        # now it's maximized
        
    else: # if the window was maximized
        expand_button.config(text=" 🗖 ")
        root.geometry(root.normal_size)
        root.maximized = not root.maximized
        # now it is not maximized

# put a close button on the title bar
close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)

# a frame for the main area of the window, this is where the actual app will go
window = Frame(root, bg=DGRAY,highlightthickness=0)

# pack the widgets
title_bar.pack(fill=X)
close_button.pack(side=RIGHT,ipadx=7,ipady=1)
expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
title_bar_title.pack(side=LEFT, padx=10)
window.pack(expand=1, fill=BOTH) # replace this with your main Canvas/Frame/etc.
#xwin=None
#ywin=None
# bind title bar motion to the move window function
# Create a custom style for the progress bar
style = ttk.Style(root)
style.theme_use("default")
style.configure("Custom.Horizontal.TProgressbar", background=PROGRESS_COLOR, troughcolor=BG_COLOR, thickness=10)


def changex_on_hovering(event):
    global close_button
    close_button['bg']='red'
    
    
def returnx_to_normalstate(event):
    global close_button
    close_button['bg']=RGRAY
    

def change_size_on_hovering(event):
    global expand_button
    expand_button['bg']=LGRAY
    
    
def return_size_on_hovering(event):
    global expand_button
    expand_button['bg']=RGRAY
    

def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=LGRAY
    
    
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=RGRAY
    

def get_pos(event): # this is executed when the title bar is clicked to move the window
    if root.maximized == False:
 
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        
        def move_window(event): # runs when window is dragged
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


        def release_window(event): # runs when window is released
            root.config(cursor="arrow")
            
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
    else:
        expand_button.config(text=" 🗖 ")
        root.maximized = not root.maximized

title_bar.bind('<Button-1>', get_pos) # so you can drag the window from the title bar
title_bar_title.bind('<Button-1>', get_pos) # so you can drag the window from the title 

# button effects in the title bar when hovering over buttons
close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
expand_button.bind('<Enter>', change_size_on_hovering)
expand_button.bind('<Leave>', return_size_on_hovering)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)

# resize the window width
resizex_widget = Frame(window,bg=DGRAY,cursor='sb_h_double_arrow')
resizex_widget.pack(side=RIGHT,ipadx=2,fill=Y)


def resizex(event):
    xwin = root.winfo_x()
    difference = (event.x_root - xwin) - root.winfo_width()
    
    if root.winfo_width() > 150 : # 150 is the minimum width for the window
        try:
            root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
        except:
            pass
    else:
        if difference > 0: # so the window can't be too small (150x150)
            try:
                root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
            except:
                pass
              
    resizex_widget.config(bg=DGRAY)

resizex_widget.bind("<B1-Motion>",resizex)

# resize the window height
resizey_widget = Frame(window,bg=DGRAY,cursor='sb_v_double_arrow')
resizey_widget.pack(side=BOTTOM,ipadx=2,fill=X)

def resizey(event):
    ywin = root.winfo_y()
    difference = (event.y_root - ywin) - root.winfo_height()

    if root.winfo_height() > 150: # 150 is the minimum height for the window
        try:
            root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
        except:
            pass
    else:
        if difference > 0: # so the window can't be too small (150x150)
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass

    resizex_widget.config(bg=DGRAY)

resizey_widget.bind("<B1-Motion>",resizey)

# some settings
root.bind("<FocusIn>",deminimize) # to view the window by clicking on the window icon on the taskbar
root.after(10, lambda: set_appwindow(root)) # to see the icon on the task bar


#YOUR CODE GOES between the lines :)
# ===================================================================================================
        

def get_name(video_path):
    if not isinstance(video_path, str) or not os.path.isfile(video_path):
        raise ValueError("Invalid file path")
    
    filename = os.path.basename(video_path)
    name, ext = os.path.splitext(filename)
    
    return name

def do_cut():
    # Create loading bar window
    loading_window = tk.Toplevel(root, bg=BG_COLOR)
    loading_window.title("Extracting Frames...")
    loading_window.geometry("400x80")

    # Create progress bar
    progress = tk.DoubleVar()
    progress.set(0)
    progress_bar = ttk.Progressbar(
        loading_window,
        variable=progress,
        maximum=frame_count,
        mode="determinate",
        length=380,
        style="Custom.Horizontal.TProgressbar"
    )
    progress_bar.pack(fill=tk.BOTH, padx=10, pady=10)

    # Create percentage label
    percentage_label = tk.Label(
        loading_window,
        text="0%",
        font=("Arial", 14),
        bg=BG_COLOR,
        fg=FG_COLOR
    )
    percentage_label.pack()

    folder_path = None
    
    if save_folder_path:
        folder_path = os.path.join(save_folder_path)
    else:
        folder_path = os.path.join(DEAFAULT_FOLDER, folder_name)
    
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    
    print(folder_path)
        
    # Iterate through the frames and extract photos
    for i in tqdm(range(frame_count)):
        # Read the frame
        success, frame = video_capture.read()

        if not success:
            break

        file_path = os.path.join(folder_path, video_path_str +  f'_frame_{i+1}.png')
        cv2.imwrite(file_path, frame)

        # Update progress bar and percentage label
        progress.set(i + 1)
        progress_bar.update()
        percentage = int((i+1)*100/frame_count)
        percentage_label.config(text=f"{percentage}%")

    # Release the video capture object
    video_capture.release()

    # Close loading bar window
    loading_window.destroy()

def choose_video():
    global video_path, video_path_str, folder_name
    video_path = filedialog.askopenfilename()
    video_path_str = get_name(video_path)
    folder_name = video_path_str + "_video_frames"

    print(video_path, video_path_str, folder_name)
    
    if video_path:
        global video_capture, frame_rate, frame_count
        video_capture = cv2.VideoCapture(video_path)
        # Set the frame rate and count
        frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        video_label.config(text=f"Video Path: {video_path}")

# Function to update folder label text
def update_folder_label_text(folder_path):
    folder_label.config(text=f"New Folder Path: {folder_path}")

# Update folder label text after choosing folder
def choose_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        save_folder_path = os.path.join(folder_path, folder_name)
        if not os.path.isdir(save_folder_path):
            os.mkdir(save_folder_path)
        update_folder_label_text(save_folder_path)

# Video path label
video_label = tk.Label(root, text="Choose a Video File to Cut:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR)
video_label.pack(pady=10)

# New folder path label
folder_label = tk.Label(root, text="Choose Folder to Store Frames:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR)
folder_label.pack(pady=10)

# Choose video button
choose_video_button = tk.Button(root, text="Choose Video", command=choose_video, font=("Arial", 12))
choose_video_button.pack(side=tk.LEFT, padx=10, pady=10)

# Choose folder button
choose_folder_button = tk.Button(root, text="Choose Folder", command=choose_folder, font=("Arial", 12))
choose_folder_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Start button
start_button = tk.Button(root, text="Start", command=do_cut, font=("Arial", 16), width=10, height=2, bg=PROGRESS_COLOR)
start_button.pack(side=tk.BOTTOM, pady=10)


root.update()
video_label.place(relx=0.5, rely=0.30, anchor="c")
folder_label.place(relx=0.5, rely=0.45, anchor="c")
start_button.place(relx=0.5, rely=0.75, anchor="c")
choose_video_button.place(relx=start_button.winfo_x() / root.winfo_width() - 0.5 / 3, rely=0.75, anchor="c")
choose_folder_button.place(relx=0.75, rely=0.75, anchor="c")


# ===================================================================================================

root.mainloop()