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
- Pip (Python package manager)
- Gunicorn (for production deployment)

## Installation

To run **Heartbeat** locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/heartbeat.git
cd heartbeat
```

### 2. Install dependencies

Ensure you have Python and pip installed, then run the following to install the required Python libraries:

```bash
pip install -r requirements.txt
```

### 3. Start the Flask server for Development

For local development, run the following command to start the Flask server:

```bash
python app.py
```

Once the server is running, you can view the **Heartbeat Dashboard** by navigating to:

```
http://127.0.0.1:5000/
```

### 4. Deploy to Production

For a production environment, it is recommended to use **Gunicorn**, a production-grade WSGI server, instead of the built-in Flask server.

#### Install Gunicorn

```bash
pip install gunicorn
```

#### Run with Gunicorn

To start the Flask application with Gunicorn, run:

```bash
gunicorn -w 4 app:app
```

- `-w 4` specifies the number of worker processes (you can adjust based on your system resources).
- `app:app` points to the `app` variable in the `app.py` file.

#### Set up Reverse Proxy with Nginx (Optional)

For better performance, security, and load balancing, you can configure a reverse proxy using **Nginx**.

Example Nginx Configuration:

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

After updating Nginx, reload the service:

```bash
sudo systemctl restart nginx
```

### 5. Viewing the Dashboard

Once the application is running in production, you can view the **Heartbeat Dashboard** by navigating to your server's IP address or domain:

```
http://your_domain.com/
```

## Code Overview

### Backend (Flask API)

The backend of **Heartbeat** is built using **Flask**, a lightweight Python web framework. The Flask app provides an API endpoint `/metrics`, which serves the current system metrics in JSON format.

Key parts of the code:

- **`get_system_metrics()`**: Gathers CPU, memory, disk, and network data using the `psutil` library.
- **`log_data()`**: Logs system metrics to a file for historical tracking.
- **`/metrics` route**: Fetches real-time system metrics.

### Frontend (Dashboard)

The dashboard is created using HTML, CSS, and JavaScript. It features **Chart.js** for visualizing the system metrics over time. 

- **Charts**: Displays real-time updates for CPU, memory, disk usage, and network activity.
- **Fetch Metrics**: Periodically fetches system metrics from the backend via the `/metrics` endpoint.

## Usage

Once the application is running, the dashboard will automatically refresh every second to update the system metrics. You will see:

- **CPU Usage**: A graph showing the current CPU usage.
- **Memory Usage**: A graph showing the current memory usage.
- **Disk Usage**: A graph showing the current disk usage.
- **Network Activity**: Graphs showing the amount of data sent and received.

You can modify the update interval and customize the dashboard by editing the `updateInterval` variable in the JavaScript section.

## Logging

Heartbeat logs all metrics into a file (`system_metrics.log`). Each entry contains the current system state, including CPU, memory, disk, and network metrics, along with the timestamp.

## Contributing

We welcome contributions! If you'd like to improve or expand **Heartbeat**, feel free to fork the project and submit a pull request.

## License

**Heartbeat** is open source and available under the GPL-3.0 license. See the LICENSE file for more details.

---

By **Xelvanta Group Systems**  
For support or inquiries, please contact us at [enquiry.information@proton.me](mailto:enquiry.information@proton.me).  
GitHub: [https://github.com/Xelvanta](https://github.com/Xelvanta)