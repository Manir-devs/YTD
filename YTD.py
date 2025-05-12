import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
import yt_dlp
import os
import subprocess

root = tk.Tk()
root.title("YT Downloader Manir Edition 😎")
root.geometry("800x600")

video_audio_list = []
selected_video = tk.StringVar()
selected_audio = tk.StringVar()
download_folder = os.path.expanduser("~/Downloads")
download_progress_label = tk.StringVar(value="")

# Single Progress bar
main_progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")


def fetch_formats():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Link daal....")
        return

    video_audio_list.clear()
    for row in format_tree.get_children():
        format_tree.delete(row)

    selected_video.set("")
    selected_audio.set("")
    main_progress.pack(pady=5)
    main_progress.config(mode="indeterminate")
    main_progress.start()
    download_progress_label.set("Fetching formats... 🔍")

    def run():
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])

                for fmt in formats:
                    fmt_id = fmt.get("format_id")
                    ext = fmt.get("ext")
                    res = fmt.get("resolution") or f"{fmt.get('width', '')}x{fmt.get('height', '')}"
                    fps = fmt.get("fps", '')
                    size = round(fmt.get("filesize", 0) / (1024*1024), 2) if fmt.get("filesize") else "?"
                    acodec = fmt.get("acodec", "none")
                    vcodec = fmt.get("vcodec", "none")

                    kind = "Video" if vcodec != "none" and acodec == "none" else "Audio" if vcodec == "none" else "AV"

                    video_audio_list.append((fmt_id, ext, res, fps, size, kind))
                    format_tree.insert('', 'end', values=(fmt_id, ext, res, fps, size, kind))
                download_progress_label.set("Formats Loaded ✅")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                download_progress_label.set("Error Aaya Bhai.. 😢")
            finally:
                main_progress.stop()
                main_progress.pack_forget()

    threading.Thread(target=run).start()


def set_selected(event):
    cur = format_tree.focus()
    values = format_tree.item(cur).get("values", [])
    if not values:
        return

    if values[-1] == "Video":
        selected_video.set(values[0])
    elif values[-1] == "Audio":
        selected_audio.set(values[0])


def show_popup(title, filepath, size):
    popup = tk.Toplevel(root)
    popup.title("Download Complete 🎉")
    popup.geometry("400x200")

    filename = os.path.basename(filepath)

    tk.Label(popup, text=f"✅ File downloaded successfully!", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(popup, text=f"File: {filename}").pack()
    tk.Label(popup, text=f"Path: {filepath}").pack()
    tk.Label(popup, text=f"Size: {size} MB").pack()

    def open_file():
        subprocess.Popen(['xdg-open', filepath])

    tk.Button(popup, text="Open Video 🎬", command=open_file).pack(pady=5)
    tk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)


def download_and_merge():
    url = url_entry.get()
    vid_id = selected_video.get()
    aud_id = selected_audio.get()

    # Folder selection
    global download_folder
    folder = filedialog.askdirectory(initialdir=download_folder, title="Select Download Foldr")
    if not folder:
        return
    download_folder = folder

    format_str = ""
    if vid_id and aud_id:
        format_str = f"{vid_id}+{aud_id}"
    elif vid_id:
        format_str = vid_id
    elif aud_id:
        format_str = aud_id
    else:
        messagebox.showerror("Error", "Kuch toh select kar bhai! Audio ya Video. select karne ka tareeka: audio ya video ka id neeche waale input me daal")
        return

    output_path = os.path.join(download_folder, "%(title)s.%(ext)s")

    ydl_opts = {
        'format': format_str,
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'progress_hooks': [download_hook],
        'quiet': True
    }

    main_progress.pack(pady=5)
    main_progress["value"] = 0
    main_progress.config(mode="determinate")
    download_progress_label.set("Download Started... 🚀")

    def run():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                filename = ydl.prepare_filename(info)
                final_file = filename.replace(".webm", ".mp4") if ".webm" in filename else filename
                size = round(os.path.getsize(final_file) / (1024 * 1024), 2)
                download_progress_label.set("Download Complete! 🎉")
                main_progress.pack_forget()
                show_popup(info.get("title", "video"), final_file, size)
        except Exception as e:
            download_progress_label.set("Download Failed! 😢")
            main_progress.pack_forget()
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run).start()


def download_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes', d.get('total_bytes_estimate', 0))
        downloaded = d.get('downloaded_bytes', 0)
        if total:
            percent = downloaded * 100 / total
            mb_down = round(downloaded / (1024 * 1024), 2)
            mb_total = round(total / (1024 * 1024), 2)
            main_progress["value"] = percent
            download_progress_label.set(f"Downloading... {mb_down:.2f} / {mb_total:.2f} MB")
            root.update_idletasks()
    elif d['status'] == 'finished':
        main_progress["value"] = 100
        download_progress_label.set("Finalizing File... 🛠️")


# --- GUI ---

tk.Label(root, text="YouTube Link daal:").pack()
url_entry = tk.Entry(root, width=100)
url_entry.pack(pady=5)

tk.Button(root, text="Fetch Formats", command=fetch_formats).pack(pady=5)

# Treeview with Scrollbar
# Treeview with Scrollbar
tree_frame = tk.Frame(root)
tree_frame.pack(expand=True, fill='both', padx=10)

xscroll = ttk.Scrollbar(tree_frame, orient='horizontal')
xscroll.pack(side='bottom', fill='x')

yscroll = ttk.Scrollbar(tree_frame)
yscroll.pack(side='right', fill='y')

format_tree = ttk.Treeview(tree_frame, 
                           columns=("ID", "Ext", "Res", "FPS", "Size (MB)", "Type"), 
                           show="headings", 
                           yscrollcommand=yscroll.set,
                           xscrollcommand=xscroll.set)
xscroll.config(command=format_tree.xview)
yscroll.config(command=format_tree.yview)

for col in format_tree["columns"]:
    format_tree.heading(col, text=col)
    format_tree.column(col, width=100, anchor='center')  # Fixed width set kar raha hu

format_tree.pack(expand=True, fill='both')
format_tree.bind("<Double-1>", set_selected)


sel_frame = tk.Frame(root)
sel_frame.pack(pady=10)

tk.Label(sel_frame, text="Selected Video Format ID:").grid(row=0, column=0, sticky="e")
tk.Entry(sel_frame, textvariable=selected_video, width=15).grid(row=0, column=1, padx=5)

tk.Label(sel_frame, text="Selected Audio Format ID:").grid(row=0, column=2, sticky="e")
tk.Entry(sel_frame, textvariable=selected_audio, width=15).grid(row=0, column=3, padx=5)

tk.Button(root, text="Download & Merge", command=download_and_merge, bg="green", fg="white").pack(pady=10)

tk.Label(root, textvariable=download_progress_label, font=("Arial", 10)).pack()

root.mainloop()
