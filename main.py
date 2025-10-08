import tkinter as tk
from tkinter import filedialog, messagebox
from video2gif import convert_videos_to_gifs, VideoConfig

videos: list[str] = []  # global list of selected files


def refresh_file_list(frame: tk.Frame, convert_button: tk.Button):
    """Update the displayed list of files with delete and settings buttons."""
    for widget in frame.winfo_children():
        widget.destroy()

    if not videos:
        tk.Label(frame, text="No file selected", anchor="w").pack(fill="x", pady=2)
        convert_button.config(state="disabled")
        return
    convert_button.config(state="active")
    for path in videos:

        row = tk.Frame(frame)
        row.pack(fill="x", padx=10, pady=2)

        tk.Button(
            row,
            text="⚙",
            command=lambda p=path: open_file_settings(p),
            fg="black",
            font=("Arial", 10, "bold"),
            width=2,
            relief="flat",
        ).pack(side="left", padx=(0, 5))

        tk.Label(row, text=path, anchor="w").pack(side="left", fill="x", expand=True)

        tk.Button(
            row,
            text="×",
            command=lambda p=path: remove_file(p, frame, convert_button),
            fg="red",
            font=("Arial", 10, "bold"),
            width=2,
            relief="flat",
        ).pack(side="right")


def open_file_settings(path: str):
    """Open a new window for per-file settings."""
    video_config = [video for video in videos if video.path == path][0]

    win = tk.Toplevel()
    win.title("Settings")
    win.geometry("300x360")

    tk.Label(win, text=path, wraplength=280, justify="left").pack(pady=10)

    # FPS
    tk.Label(win, text="FPS:").pack()
    fps_var = tk.IntVar(value=video_config.fps)
    tk.Entry(win, textvariable=fps_var).pack()

    # Resolution
    tk.Label(win, text="Resolution:").pack()
    res_var = tk.IntVar(value=video_config.resolution)
    tk.Entry(win, textvariable=res_var).pack()

    # Length chosen
    is_length_chosen_var = tk.BooleanVar(value=video_config.is_length_chosen)

    def toggle_length_fields():
        if is_length_chosen_var.get():
            start_entry.config(state="normal")
            end_entry.config(state="normal")
            start_var.set(video_config.start)
            end_var.set(video_config.end)
        else:
            start_var.set(0)
            end_var.set("until the video ends")
            start_entry.config(state="disabled")
            end_entry.config(state="disabled")

    tk.Checkbutton(
        win,
        text="Custom start/end",
        variable=is_length_chosen_var,
        command=toggle_length_fields,
    ).pack(pady=5)

    tk.Label(win, text="Start (sec):").pack()
    start_var = tk.DoubleVar(value=video_config.start if video_config.is_length_chosen else 0)
    start_entry = tk.Entry(win, textvariable=start_var)
    start_entry.pack()
    start_entry.config(state="disabled")

    tk.Label(win, text="End (sec):").pack()
    end_var = tk.StringVar(
        value=str(video_config.end) if video_config.is_length_chosen else "until the video ends"
    )
    end_entry = tk.Entry(win, textvariable=end_var)
    end_entry.pack()
    end_entry.config(state="disabled")

    # Apply initial state based on checkbox
    if not video_config.is_length_chosen:
        start_entry.config(state="disabled")
        end_entry.config(state="disabled")

    def save_settings():
        end_value = end_var.get()
        try:
            end_value = float(end_value)
        except ValueError:
            end_value = "until the video ends"

        video_config.fps = fps_var.get()
        video_config.resolution = res_var.get()
        video_config.is_length_chosen = is_length_chosen_var.get()
        if video_config.is_length_chosen:
            video_config.start = start_var.get()
            video_config.end = end_var.get()

        win.destroy()

    tk.Button(win, text="Save", command=save_settings).pack(pady=15)


def add_files(file_frame: tk.Frame, more_files_button: tk.Button, convert_button: tk.Button):
    global videos
    new_paths = filedialog.askopenfilenames(title="Select files")
    if new_paths:
        for current_path in new_paths:
            videos.append(VideoConfig(path=current_path))
        more_files_button.config(state="normal")
        refresh_file_list(file_frame, convert_button)


def add_more_files(file_frame: tk.Frame, convert_button: tk.Button) -> None:
    global videos
    new_paths = filedialog.askopenfilenames(title="Select more files")
    new_paths = [path for path in new_paths if path not in videos]
    if new_paths:
        for current_path in new_paths:
            videos.append(VideoConfig(path=current_path))
        refresh_file_list(file_frame, convert_button)
        convert_button.config(state="normal")


def remove_file(path: str, frame: tk.Frame, convert_button: tk.Button):
    global videos
    videos = [p for p in videos if p != path]
    refresh_file_list(frame, convert_button)


def convert_to_gif():
    global videos
    if videos:
        print("Converting videos to GIFs with settings:")
        for p in videos:
            convert_videos_to_gifs(videos)
            print("Conversion complete!")


# ✅ New function for the 📁 button
def choose_destination(destination_var: tk.StringVar):
    folder = filedialog.askdirectory(title="Select destination folder")
    if folder:
        destination_var.set(folder)



def run():
    root = tk.Tk()
    root.title("Vid2Gif")
    root.geometry("400x430")
    icon = tk.PhotoImage(file = "icon.png")
    root.iconphoto(True, icon)

    file_frame = tk.Frame(root)
    file_frame.pack(pady=15, fill="both", expand=True)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    more_files_button = tk.Button(
        button_frame,
        text="Add more files",
        state="disabled",
        command=lambda: add_more_files(file_frame, convert_button),
    )
    more_files_button.pack(side="right", padx=5)

    add_files_button = tk.Button(
        button_frame,
        text="Add files",
        command=lambda: add_files(file_frame, more_files_button, convert_button),
    )
    add_files_button.pack(side="left", padx=5)

    # ✅ Destination field + button (NEW)
    dest_frame = tk.Frame(root)
    dest_frame.pack(pady=10, fill="x", padx=15)

    tk.Label(dest_frame, text="Destination:").pack(side="left")

    destination_var = tk.StringVar()
    destination_entry = tk.Entry(dest_frame, textvariable=destination_var)
    destination_entry.pack(side="left", fill="x", expand=True, padx=5)

    # Now uses the new function
    tk.Button(
        dest_frame,
        text="📁",
        width=3,
        command=lambda: choose_destination(destination_var),
    ).pack(side="left")
    # Access anywhere: destination_var.get()

    convert_button = tk.Button(
        root, text="Convert to gif!", state="disabled", command=convert_to_gif
    )
    convert_button.pack(pady=20)

    refresh_file_list(file_frame, convert_button)
    root.mainloop()


if __name__ == "__main__":
    run()
    print("Final selected files:", videos)
