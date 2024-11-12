import os
import sys
import subprocess
import ctypes
import platform

def request_admin_privileges():
    """Request administrative privileges based on OS."""
    if platform.system() == "Windows":
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            script = sys.argv[0]
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
            sys.exit(0)
    elif platform.system() in ("Linux", "Darwin"):
        if os.geteuid() != 0:
            print("This script requires elevated privileges.")
            subprocess.check_call(['sudo', 'python3'] + sys.argv)
            sys.exit(0)

def launch_app():
    """Launch the app.py in a new terminal window."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if platform.system() == "Windows":
        subprocess.run(['start', 'cmd', '/K', f'cd {script_dir} && python app.py'], shell=True)
    elif platform.system() == "Darwin":
        subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "cd {script_dir} && python3 app.py"'])
    elif platform.system() == "Linux":
        subprocess.run(['gnome-terminal', '--', 'bash', '-c', f'cd {script_dir} && python3 app.py'])

if __name__ == "__main__":
    request_admin_privileges()

    launch_app()