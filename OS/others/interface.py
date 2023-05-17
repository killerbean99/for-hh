# def change_fps():
#     fps_window = tk.Toplevel(root)
#     fps_window.title("Change FPS")

#     fps_label = tk.Label(fps_window, text="Enter FPS:")
#     fps_label.pack()

#     fps_entry = tk.Entry(fps_window)
#     fps_entry.pack()

#     def apply_fps():
#         global frame_rate
#         frame_rate = float(fps_entry.get())
#         print(f"New FPS: {frame_rate}")
#         fps_window.destroy()

#     apply_button = tk.Button(fps_window, text="Apply", command=apply_fps)
#     apply_button.pack()