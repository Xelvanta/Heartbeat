import tkinter as tk
import psutil
import GPUtil
import signal
import sys
from threading import Thread
import time
import config

def get_gpu_metrics():
    # Get the first available GPU (assuming single GPU, modify if multiple GPUs)
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        gpu_usage = gpu.load * 100  # load is a fraction, so multiply by 100 to get a percentage
        gpu_memory = gpu.memoryUtil * 100  # same as above
        gpu_temp = gpu.temperature
        return {
            'usage': gpu_usage,
            'memory': gpu_memory,
            'temperature': gpu_temp
        }
    return {'usage': 0, 'memory': 0, 'temperature': 0}

def get_system_metrics():
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network = psutil.net_io_counters()
    gpu = get_gpu_metrics()
    
    metrics = {
        'cpu': cpu,
        'memory': memory,
        'disk': disk,
        'network': {
            'sent': network.bytes_sent,
            'recv': network.bytes_recv
        },
        'gpu': gpu
    }
    return metrics

def update_overlay():
    metrics = get_system_metrics()

    if 'cpu' in metrics and 'memory' in metrics and 'disk' in metrics and 'network' in metrics and 'gpu' in metrics:
        cpu_label.config(text=f"CPU: {metrics['cpu']}%")
        disk_label.config(text=f"Disk: {metrics['disk']}%")
        network_sent_label.config(text=f"Sent: {metrics['network']['sent']} bytes")
        network_recv_label.config(text=f"Received: {metrics['network']['recv']} bytes")

        memory_label.config(text=f"Memory: {metrics['memory']}%")
        if metrics['memory'] > config.FATAL_THRESHOLD:
            memory_label.config(fg="red")  # FATAL level
        elif metrics['memory'] > config.CRITICAL_THRESHOLD:
            memory_label.config(fg="orange")  # CRITICAL level
        elif metrics['memory'] > config.WARNING_THRESHOLD:
            memory_label.config(fg="yellow")  # WARNING level
        else:
            memory_label.config(fg="white")

        # GPU metrics display
        gpu_usage_label.config(text=f"GPU Usage: {metrics['gpu']['usage']}%")
        gpu_memory_label.config(text=f"GPU Memory: {metrics['gpu']['memory']}%")
        gpu_temp_label.config(text=f"GPU Temp: {metrics['gpu']['temperature']}°C")

    root.after(1000, update_overlay)

def start_overlay():
    global root
    root = tk.Tk()
    root.title("System Metrics Overlay")

    overlay_width = 250
    overlay_height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_pos = 10
    y_pos = screen_height - overlay_height - 10

    root.geometry(f"{overlay_width}x{overlay_height}+{x_pos}+{y_pos}")

    root.overrideredirect(True)

    root.configure(bg='black')
    root.attributes('-transparentcolor', 'black')
    root.attributes("-topmost", True)

    font = ("Helvetica", 10)

    global cpu_label, memory_label, disk_label, network_sent_label, network_recv_label
    global gpu_usage_label, gpu_memory_label, gpu_temp_label

    cpu_label = tk.Label(root, text="CPU: Loading...", fg="white", bg="black", font=font)
    cpu_label.pack(pady=2)

    memory_label = tk.Label(root, text="Memory: Loading...", fg="white", bg="black", font=font)
    memory_label.pack(pady=2)

    disk_label = tk.Label(root, text="Disk: Loading...", fg="white", bg="black", font=font)
    disk_label.pack(pady=2)

    network_sent_label = tk.Label(root, text="Sent: Loading...", fg="white", bg="black", font=font)
    network_sent_label.pack(pady=2)

    network_recv_label = tk.Label(root, text="Received: Loading...", fg="white", bg="black", font=font)
    network_recv_label.pack(pady=2)

    # GPU metrics labels
    gpu_usage_label = tk.Label(root, text="GPU Usage: Loading...", fg="white", bg="black", font=font)
    gpu_usage_label.pack(pady=2)

    gpu_memory_label = tk.Label(root, text="GPU Memory: Loading...", fg="white", bg="black", font=font)
    gpu_memory_label.pack(pady=2)

    gpu_temp_label = tk.Label(root, text="GPU Temp: Loading...", fg="white", bg="black", font=font)
    gpu_temp_label.pack(pady=2)

    update_overlay()

    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()

def handle_exit_signal(signal, frame):
    root.quit()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit_signal)
    start_overlay()