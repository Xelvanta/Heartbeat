import os
import urllib.request
import tkinter as tk
from tkinter import filedialog, messagebox
import ctypes
import tempfile
import shutil
import subprocess
import sys
import time
import threading
import stat

def request_admin_privileges():
    if sys.platform == "win32":
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            script = sys.argv[0]
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
            sys.exit(0)
    elif sys.platform in ("linux", "darwin"):
        if os.geteuid() != 0:
            print("This script requires elevated privileges.")
            subprocess.check_call(['sudo', 'python3'] + sys.argv)
            sys.exit(0)

def download_favicon():
    url = "https://raw.githubusercontent.com/Xelvanta/Heartbeat/main/static/HeartbeatIcon512px.png"
    temp_dir = tempfile.mkdtemp()
    temp_icon_path = os.path.join(temp_dir, "HeartbeatIcon512px.png")
    try:
        urllib.request.urlretrieve(url, temp_icon_path)
        return temp_icon_path, temp_dir
    except Exception as e:
        print(f"Failed to download favicon: {e}")
        return None, None

def cleanup_temp_folder(temp_dir):
    if temp_dir and os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Failed to delete temp folder: {e}")

def clone_and_install(repo_url, install_dir, run_app):
    try:
        subprocess.run(["git", "clone", repo_url, install_dir], check=True)
        os.chdir(install_dir)
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        messagebox.showinfo("Success", "Installation completed successfully!")
        
        if run_app:
            subprocess.Popen(["python", "app.py"])
        
        root.destroy()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Installation failed: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

def browse_folder():
    folder_path = filedialog.askdirectory(title="Choose Installation Directory")
    if folder_path:
        install_dir_var.set(folder_path)

def start_countdown(button, countdown_time):
    for i in range(countdown_time, 0, -1):
        button.config(text=f"Yes ({i})")
        button.update()
        time.sleep(1)
    button.config(state=tk.NORMAL)
    button.config(text="Yes")

def show_centered_popup(confirm_window, root):
    confirm_window.update_idletasks()
    window_width = confirm_window.winfo_width()
    window_height = confirm_window.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    confirm_window.geometry(f"+{x_position}+{y_position}")

def handle_permission_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_files_in_folder(install_dir):
    for filename in os.listdir(install_dir):
        file_path = os.path.join(install_dir, filename)
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path, onerror=handle_permission_error)
            else:
                os.remove(file_path)
        except PermissionError:
            print(f"Permission denied: {file_path}. Skipping...")
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping...")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

def final_delete_confirmation(install_dir, confirm_window, repo_url, run_app):
    def on_final_yes_click():
        delete_files_in_folder(install_dir)
        confirm_window.destroy()
        clone_and_install(repo_url, install_dir, run_app)
        confirm_window.destroy()

    def on_final_no_click():
        messagebox.showinfo("Operation Cancelled", "The operation has been cancelled. Please select an empty folder.")
        confirm_window.destroy()

    confirm_window = tk.Toplevel(root)
    confirm_window.title("Final Confirmation")

    label = tk.Label(confirm_window, text="The following files will be permanently deleted.\nAre you sure you want to proceed?\nThis action is irreversible.")
    label.pack(padx=20, pady=10)

    file_list_frame = tk.Frame(confirm_window)
    file_list_frame.pack(pady=5, padx=20, fill="both", expand=True)

    file_list_box = tk.Text(file_list_frame, wrap="none", height=10, width=50)
    file_list_box.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(file_list_frame, orient="vertical", command=file_list_box.yview)
    scrollbar.pack(side="right", fill="y")
    file_list_box.config(yscrollcommand=scrollbar.set)

    for root_dir, dirs, files in os.walk(install_dir):
        for name in dirs + files:
            file_list_box.insert("end", f"{os.path.join(root_dir, name)}\n")
    file_list_box.config(state="disabled")

    button_frame = tk.Frame(confirm_window)
    button_frame.pack(pady=10)

    yes_button = tk.Button(button_frame, text="Yes", command=on_final_yes_click, state=tk.DISABLED)
    yes_button.pack(side="left", padx=10)

    no_button = tk.Button(button_frame, text="Cancel", command=on_final_no_click)
    no_button.pack(side="right", padx=10)

    countdown_thread = threading.Thread(target=start_countdown, args=(yes_button, 5))
    countdown_thread.start()
    show_centered_popup(confirm_window, root)

def confirm_and_cleanup_folder(install_dir, repo_url, run_app):
    if os.listdir(install_dir):
        def on_yes_click():
            confirm_window.destroy()
            final_delete_confirmation(install_dir, confirm_window, repo_url, run_app)

        def on_no_click():
            messagebox.showinfo("Operation Cancelled", "The operation has been cancelled. Please select an empty folder.")
            confirm_window.destroy()

        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirm Folder Cleanup")

        label = tk.Label(confirm_window, text="The selected folder is not empty.\nDo you want to delete all its contents before proceeding?\nThis action cannot be undone.", justify="center")
        label.pack(padx=20, pady=15)

        button_frame = tk.Frame(confirm_window)
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Yes", command=on_yes_click, state=tk.DISABLED)
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = tk.Button(button_frame, text="No", command=on_no_click)
        no_button.pack(side=tk.LEFT, padx=10)

        countdown_thread = threading.Thread(target=start_countdown, args=(yes_button, 5))
        countdown_thread.start()
        show_centered_popup(confirm_window, root)
    else:
        clone_and_install(repo_url, install_dir, run_app)

def start_installation():
    repo_url = "https://github.com/Xelvanta/Heartbeat"
    install_dir = install_dir_var.get()
    run_app = run_app_var.get()

    if not install_dir:
        messagebox.showerror("Error", "Please select an installation directory.")
        return

    if not os.path.exists(install_dir):
        messagebox.showerror("Error", "The selected folder does not exist.")
        return

    confirm_and_cleanup_folder(install_dir, repo_url, run_app)

def minimize_terminal():
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

root = tk.Tk()
root.title("Heartbeat Installer")

window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

icon_path, temp_dir = download_favicon()

if icon_path and os.path.exists(icon_path):
    root.iconphoto(False, tk.PhotoImage(file=icon_path))
else:
    print("Icon file not available.")

root.protocol("WM_DELETE_WINDOW", lambda: (cleanup_temp_folder(temp_dir), root.destroy()))

install_dir_var = tk.StringVar()
run_app_var = tk.BooleanVar(value=True)

tk.Label(root, text="Select Installation Directory:").pack(pady=10)
tk.Entry(root, textvariable=install_dir_var, width=40).pack(pady=5)
tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)
tk.Checkbutton(root, text="Run application after installation", variable=run_app_var).pack(pady=10)
tk.Button(root, text="Install", command=start_installation).pack(pady=15)

request_admin_privileges()
minimize_terminal()
root.mainloop()