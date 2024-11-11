import logging
import psutil
import asyncio
import time
import config

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

async def get_system_metrics():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network = psutil.net_io_counters()

    return {'cpu': cpu, 'memory': memory, 'disk': disk, 'network': {
        'sent': network.bytes_sent, 'recv': network.bytes_recv}}

async def monitor_system():
    while True:
        metrics = await get_system_metrics()
        await log_data(metrics)
        await asyncio.sleep(config.LOG_FREQUENCY)

if __name__ == '__main__':
    asyncio.run(monitor_system())