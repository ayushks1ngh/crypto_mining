import psutil
import platform
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.stats = {
            'cpu_usage': 0,
            'memory_usage': 0,
            'temperature': 0,
            'uptime': 0
        }

    def get_stats(self):
        self.stats.update({
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'temperature': self._get_temperature(),
            'uptime': self._get_uptime()
        })
        return self.stats

    def _get_temperature(self):
        try:
            if platform.system() == 'Linux':
                temp = psutil.sensors_temperatures()
                if 'cpu_thermal' in temp:
                    return temp['cpu_thermal'][0].current
            return 0
        except:
            return 0

    def _get_uptime(self):
        return int((datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds())