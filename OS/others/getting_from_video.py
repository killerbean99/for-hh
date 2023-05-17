import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tqdm import tqdm
import cv2

# Define the colors for the dark theme
BG_COLOR = "#1C1C1C"
FG_COLOR = "#F8F8FF"
BUTTON_BG_COLOR = "#4A4A4A"
BUTTON_FG_COLOR = "#F8F8FF"
PROGRESS_COLOR = "#00BFFF"
DEAFAULT_FOLDER = os.getcwd()
new_folder_path = None
        

# def get_name(video_path):
#     video_path = 



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

    if new_folder_path:
        folder_path = new_folder_path
    else:
        folder_name = "Video Frames"
        folder_path = os.path.join(DEAFAULT_FOLDER, folder_name)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        
    # Iterate through the frames and extract photos
    for i in tqdm(range(frame_count)):
        # Read the frame
        success, frame = video_capture.read()

        if not success:
            break
        # video_path_str = get_name(video_path)
        file_path = os.path.join(folder_path, f'frame_{i+1}.png')
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
    global video_path
    video_path = filedialog.askopenfilename()
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
        new_folder_name = "Video Frames"
        new_folder_path = os.path.join(folder_path, new_folder_name)
        if not os.path.isdir(new_folder_path):
            os.mkdir(new_folder_path)
        update_folder_label_text(new_folder_path)

# Main window
root = tk.Tk()
root.title("Cut Video")
root.resizable(width=False, height=False)
root.geometry("800x240+560+400")
root.config(bg=BG_COLOR)


# Create a custom style for the progress bar
style = ttk.Style(root)
style.theme_use("default")
style.configure("Custom.Horizontal.TProgressbar", background=PROGRESS_COLOR, troughcolor=BG_COLOR, thickness=10)

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
video_label.place(relx=0.5, rely=0.2, anchor="c")
folder_label.place(relx=0.5, rely=0.35, anchor="c")
start_button.place(relx=0.5, rely=0.7, anchor="c")
choose_video_button.place(relx=start_button.winfo_x() / root.winfo_width() - 0.5 / 3, rely=0.7, anchor="c")
choose_folder_button.place(relx=0.75, rely=0.7, anchor="c")


root.mainloop()
