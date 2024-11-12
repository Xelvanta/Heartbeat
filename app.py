import logging
import psutil
import subprocess
import asyncio
from flask import Flask, render_template, jsonify
import time
import config

app = Flask(__name__)

logging.basicConfig(filename=config.LOG_FILE, level=config.LOG_LEVEL, 
                    format='%(asctime)s - %(message)s')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

async def log_data(metrics):
    if metrics['memory'] >= config.FATAL_THRESHOLD:
        logging.critical(f"FATAL | Memory usage is at {metrics['memory']}%. System is fatally low on memory and at risk of immediate failure.")
    elif metrics['memory'] >= config.CRITICAL_THRESHOLD:
        logging.critical(f"CRITICAL | Memory usage is at {metrics['memory']}%. System is critically low on memory.")
    elif metrics['memory'] >= config.WARNING_THRESHOLD:
        logging.warning(f"WARNING | Memory usage is at {metrics['memory']}%.")

    log_message = f"CPU: {metrics['cpu']}% | Memory: {metrics['memory']}% | Disk: {metrics['disk']}% | " \
                  f"Network Sent: {metrics['network']['sent']} bytes | Network Recv: {metrics['network']['recv']} bytes"
    logging.info(log_message)

def get_system_metrics():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network = psutil.net_io_counters()
    
    metrics = {
        'cpu': cpu,
        'memory': memory,
        'disk': disk,
        'network': {
            'sent': network.bytes_sent,
            'recv': network.bytes_recv
        }
    }

    # Run the async logging within the synchronous function
    asyncio.run(log_data(metrics))
    
    return metrics

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics', methods=['GET'])
def metrics():
    metrics = get_system_metrics()
    return jsonify(metrics)

if __name__ == '__main__':
    if config.OVERLAY_ENABLED:
        subprocess.Popen(['python', 'overlay.py'])

    if config.FLASK_ENABLED:
        app.run(debug=False, use_reloader=False)
    else:
        while True:
            get_system_metrics()
            time.sleep(config.LOG_FREQUENCY)