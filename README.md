# Heartbeat - Real-Time System Monitoring Dashboard

**Heartbeat** is a lightweight, real-time monitoring tool designed to track the health and performance of systems and applications. It provides an intuitive dashboard displaying key metrics such as CPU usage, memory consumption, disk space, and network activity, enabling you to quickly identify and address system issues.

## Features

- **CPU Usage**: Real-time monitoring of CPU load.
- **Memory Usage**: Track memory consumption percentage.
- **Disk Usage**: Monitor available disk space and usage.
- **Network Activity**: View the amount of data sent and received over the network.
- **Logging**: Automatically logs key metrics with timestamps.

## Requirements

- Python 3.x
- Pip (Python package manager; usually comes with Python)
- Gunicorn (for production deployment)

## Installation

You can install **Heartbeat** and run it locally using one of the following methods:

### Option 1: Clone the Repository and Install Dependencies Manually

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/heartbeat.git
   cd heartbeat
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Use the Installer Script (Recommended for Non-Developers)

This option provides a simple installation through a script that automatically handles setup. You can use the `Heartbeat_Installer.py` script, which will automatically clone the repository into your desired directory and install all necessary dependencies:

1. Download the `Heartbeat_Installer.py` script from the repository.
2. Run the script, enter a directory into the prompt, and it will handle the cloning and installation automatically.

## Running the Application

Once you've installed **Heartbeat**, you can run it using one of the following methods:

### Option 1: Manual Setup (Development)

To start the Flask server for development:

```bash
python app.py
```

### Option 2: Use the Launcher Script (Development)

For convenience, you can run the `Heartbeat_Launcher.py` script directly from the folder where you cloned the repository. The script will automatically navigate to the correct directory and launch the app:

1. Using a file explorer, open the folder where the repository was cloned.
2. Once you're in the correct folder, double-click `Heartbeat_Launcher.py` to run it.

### Heartbeat Dashboard

Once the server is running, access the **Heartbeat Dashboard** by navigating to:

```
http://127.0.0.1:5000/
```

## Deploy to Production

For production use, it’s recommended to use **Gunicorn**, a production-grade WSGI server, instead of the Flask development server.

### Install Gunicorn

```bash
pip install gunicorn
```

### Run with Gunicorn

To start the application with Gunicorn:

```bash
gunicorn -w 4 app:app
```

- `-w 4` specifies the number of worker processes (adjust based on system resources).
- `app:app` points to the `app` variable in the `app.py` file.

You can also bind Gunicorn to `0.0.0.0:8000` if using a reverse proxy (e.g., Nginx):

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Set Up Reverse Proxy with Nginx (Optional)

For better performance, security, and load balancing, you can configure a reverse proxy with **Nginx**.

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Gunicorn will run on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

After updating Nginx, restart the service:

```bash
sudo systemctl restart nginx
```

### Viewing the Dashboard

Once the application is running in production, navigate to your server's IP address or domain to view the **Heartbeat Dashboard**:

```
http://your_domain.com/
```

## Code Overview

### Backend (Flask API)

The backend of **Heartbeat** uses **Flask**, a lightweight Python web framework, to serve the system metrics via an API endpoint `/metrics` in JSON format.

Key components:

- **`get_system_metrics()`**: Gathers CPU, memory, disk, and network data using the `psutil` library.
- **`log_data()`**: Logs system metrics to a file for historical tracking.
- **`/metrics` route**: Fetches real-time system metrics.

### Frontend (Dashboard)

The dashboard is created using HTML, CSS, and JavaScript, with **Chart.js** to visualize system metrics in real-time.

- **Charts**: Displays real-time graphs for CPU, memory, disk usage, and network activity.
- **Fetch Metrics**: Periodically fetches system metrics from the backend via the `/metrics` endpoint.

## Usage

Once **Heartbeat** is running, the dashboard will automatically refresh every second to update the system metrics. You will see:

- **CPU Usage**: Graph showing the current CPU load.
- **Memory Usage**: Graph showing memory consumption.
- **Disk Usage**: Graph showing available disk space.
- **Network Activity**: Graphs showing the amount of data sent and received.

You can modify the update interval and customize the dashboard by editing the `updateInterval` variable in the JavaScript section.

## Logging

**Heartbeat** logs system metrics to a file (`system_metrics.log`). Each log entry includes CPU, memory, disk, and network data, along with a timestamp.

## Contributing

We welcome contributions! Feel free to fork the project and submit a pull request if you’d like to help improve or expand **Heartbeat**.

## License

**Heartbeat** is open source and available under the GPL-3.0 license. See the LICENSE file for more details.

---

By **Xelvanta Group Systems**  
For support or inquiries, please contact us at [enquiry.information@proton.me](mailto:enquiry.information@proton.me).  
GitHub: [https://github.com/Xelvanta](https://github.com/Xelvanta)