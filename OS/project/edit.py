import os
import cv2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tqdm import tqdm
from natsort import natsorted


BG_COLOR = "#1C1C1C"
FG_COLOR = "#F8F8FF"
BUTTON_BG_COLOR = "#4A4A4A"
BUTTON_FG_COLOR = "#F8F8FF"
PROGRESS_COLOR = "#00BFFF"
DEAFAULT_FOLDER = os.getcwd()

save_folder_path = None
tk_title = "Cut Video"

root=tk.Tk()
root.title(tk_title)
root.geometry("800x240+560+400")
root.config(bg=BG_COLOR)


def images_to_video(image_folder, output_path, fps):
    images = natsorted([img for img in os.listdir(image_folder) if img.endswith(".png")], key=lambda y: y.lower())
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def change_fps():
    fps_window = tk.Toplevel(root)
    fps_window.title("Change FPS")
    fps_window.geometry("360x220+780+410")
    fps_window.config(bg=BG_COLOR)

    fps_label = tk.Label(fps_window, text="Enter FPS:", font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR)
    fps_label.pack(pady=10)

    fps_entry = tk.Entry(fps_window, text="Enter FPS:", font=("Arial", 20), bg=BG_COLOR, fg=FG_COLOR, borderwidth=5)
    fps_entry.pack(pady=10)

    def apply_fps():
        global fps
        fps = float(fps_entry.get())
        print(f"New FPS: {(frame_count / frame_rate):.2f}")
        fps_window.destroy()

    apply_button = tk.Button(fps_window, width=10, height=2, text="Apply", font=("Arial", 16), command=apply_fps, bg=PROGRESS_COLOR)
    apply_button.pack(pady=20)


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
    loading_window.geometry("400x80+760+500")

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
        folder_path = save_folder_path
    else:
        folder_path = os.path.join(DEAFAULT_FOLDER, folder_name)
    
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)


    x = 1
    # Iterate through the frames and extract photos
    for i in tqdm(range(frame_count)):
        # Read the frame
        success, frame = video_capture.read()

        if not success:
            break

        if fps < frame_rate:
            if i % (frame_rate / fps) == 0:
                file_path = os.path.join(folder_path, video_path_str +  f'_frame_{x}.png')
                cv2.imwrite(file_path, frame)
                x += 1
        else:
            file_path = os.path.join(folder_path, video_path_str +  f'_frame_{i+1}.png')
            cv2.imwrite(file_path, frame)

        # Update progress bar and percentage label
        progress.set(i + 1)
        progress_bar.update()
        percentage = int((i+1)*100/frame_count)
        percentage_label.config(text=f"{percentage}%")

    video_name = os.path.join(folder_path, folder_name + '_video.mp4')

    images_to_video(folder_path, video_name, fps)

    # Release the video capture object
    video_capture.release()

    # Close loading bar window
    loading_window.destroy()

def choose_video():
    global video_path, video_path_str, folder_name
    video_path = filedialog.askopenfilename()
    video_path_str = get_name(video_path)
    folder_name = video_path_str + "_frames"

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
    save_folder_path = filedialog.askdirectory()
    if save_folder_path:
        save_folder_path = os.path.join(save_folder_path, folder_name)
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

# fps
fps_button = tk.Button(root, text="FPS", command=change_fps, font=("Arial", 16), width=10, height=2, bg=BUTTON_FG_COLOR)
fps_button.pack(side=tk.BOTTOM, pady=10)

# Start button
start_button = tk.Button(root, text="Start", command=do_cut, font=("Arial", 16), width=10, height=2, bg=PROGRESS_COLOR)
start_button.pack(side=tk.BOTTOM, pady=10)


root.update()
video_label.place(relx=0.5, rely=0.2, anchor="c")
folder_label.place(relx=0.5, rely=0.35, anchor="c")
start_button.place(relx=0.6, rely=0.7, anchor="c")
fps_button.place(relx=0.4, rely=0.7, anchor="c")
choose_video_button.place(relx=0.15, rely=0.7, anchor="c")
choose_folder_button.place(relx=0.85, rely=0.7, anchor="c")

root.mainloop()