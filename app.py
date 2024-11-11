import logging
from flask import Flask, render_template, jsonify
import psutil
from datetime import datetime

app = Flask(__name__)

# Set up logging with different levels
logging.basicConfig(filename='system_metrics.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def get_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network = psutil.net_io_counters()
    metrics = {'cpu': cpu, 'memory': memory, 'disk': disk, 'network': {
        'sent': network.bytes_sent, 'recv': network.bytes_recv}}

    log_data(metrics)
    
    return metrics

def log_data(metrics):
    # Memory thresholds
    WARNING_THRESHOLD = 90
    CRITICAL_THRESHOLD = 95
    FATAL_THRESHOLD = 99

    if metrics['memory'] >= FATAL_THRESHOLD:
        logging.critical(f"FATAL | Memory usage is at {metrics['memory']}%. System is fatally low on memory and at risk of immediate failure.")
    elif metrics['memory'] >= CRITICAL_THRESHOLD:
        logging.critical(f"CRITICAL | Memory usage is at {metrics['memory']}%. System is critically low on memory.")
    elif metrics['memory'] >= WARNING_THRESHOLD:
        logging.warning(f"WARNING | Memory usage is at {metrics['memory']}%.")

    log_message = f"CPU: {metrics['cpu']}% | Memory: {metrics['memory']}% | Disk: {metrics['disk']}% | " \
                  f"Network Sent: {metrics['network']['sent']} bytes | Network Recv: {metrics['network']['recv']} bytes"
    logging.info(log_message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics', methods=['GET'])
def metrics():
    metrics = get_system_metrics()
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)