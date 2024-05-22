import cut_detect
import tkinter as tk
from tkinter import filedialog, messagebox

class VideoProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Processing App")

        self.video_path = ""
        self.output_path = ""

        self.create_widgets()

    def create_widgets(self):
        self.select_video_button = tk.Button(self.root, text="Select Video", command=self.select_video)
        self.select_video_button.pack(pady=10)

        self.select_output_button = tk.Button(self.root, text="Select Output Path", command=self.select_output)
        self.select_output_button.pack(pady=10)

        self.process_button = tk.Button(self.root, text="Process Video", command=self.process_video)
        self.process_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def select_video(self):
        self.video_path = filedialog.askopenfilename()
        if self.video_path:
            self.status_label.config(text=f"Selected video: {self.video_path}")
        else:
            self.status_label.config(text="No video selected.")

    def select_output(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if self.output_path:
            self.status_label.config(text=f"Output path: {self.output_path}")
        else:
            self.status_label.config(text="No output path selected.")

    def process_video(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please select a video file.")
            return
        if not self.output_path:
            messagebox.showerror("Error", "Please select an output path.")
            return

        self.status_label.config(text="Processing...")
        self.root.update_idletasks()
        try:
            main(self.video_path, self.output_path)
            self.status_label.config(text=f"Processing completed. Saved to: {self.output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.update()

    app = VideoProcessingApp(root)
    root.deiconify()
    root.mainloop()
