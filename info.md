# Crypto Mining Assistant Application

## Overview
This application is designed to assist users with cryptocurrency mining on a Raspberry Pi. It provides tools to monitor mining performance, manage configurations, and optimize mining operations. The app is lightweight and tailored for Raspberry Pi hardware.

---

## Features
1. **Mining Management**: Start, stop, and monitor mining operations.
2. **Performance Metrics**: Display real-time mining statistics such as hash rate, temperature, and power usage.
3. **Configuration Management**: Easily update mining pool details and wallet addresses.
4. **Remote Access**: Access the application remotely via a web interface.
5. **Hardware Optimization**: Optimize Raspberry Pi settings for efficient mining.

---

## Requirements
### Hardware
- Raspberry Pi 4 (recommended) or Raspberry Pi 3
- MicroSD card (16GB or larger)
- Power supply for Raspberry Pi
- Optional: Cooling fan or heatsink for Raspberry Pi

### Software
- Raspberry Pi OS (32-bit or 64-bit)
- Python 3.9 or higher
- Mining software (e.g., `cpuminer`, `cgminer`, or `bfgminer`)

---

## Installation Steps
1. **Set Up Raspberry Pi**:
   - Install Raspberry Pi OS on the microSD card.
   - Boot up the Raspberry Pi and connect it to the internet.

2. **Install Dependencies**:
   - Update the system:
     ```bash
     sudo apt update && sudo apt upgrade -y
     ```
   - Install Python and required libraries:
     ```bash
     sudo apt install python3 python3-pip git -y
     ```

3. **Clone the Repository**:
   - Clone the project repository into your Raspberry Pi:
     ```bash
     git clone https://github.com/your-repo/crypto-mining-assistant.git
     cd crypto-mining-assistant
     ```

4. **Install Python Dependencies**:
   - Install the required Python packages:
     ```bash
     pip3 install -r requirements.txt
     ```

5. **Set Up Mining Software**:
   - Install a mining software like `cpuminer`:
     ```bash
     sudo apt install cpuminer -y
     ```
   
   - Create a configuration file for cpuminer:
     ```bash
     nano ~/mining-config.json
     ```
   
   - Add the following configuration (example for mining Monero):
     ```json
     {
         "url": "pool.supportxmr.com:3333",
         "user": "YOUR_WALLET_ADDRESS",
         "pass": "worker1",
         "algo": "cryptonight",
         "threads": 3,
         "cpu-priority": 2,
         "retry-pause": 5
     }
     ```

   - Common Mining Pools for Beginners:
     - Monero (XMR): supportxmr.com, nanopool.org
     - Dogecoin: pool.systm.org
     - Litecoin: litecoinpool.org

   - Basic Performance Settings:
     ```bash
     # Run cpuminer with specific parameters
     cpuminer -c ~/mining-config.json --cpu-priority 2 --threads=3
     ```

   - Troubleshooting Tips:
     1. If mining software fails to start:
        ```bash
        # Check system logs
        sudo dmesg | tail
        # Check mining logs
        tail -f ~/.cpuminer/cpuminer.log
        ```
     
     2. If experiencing overheating:
        ```bash
        # Monitor temperature
        vcgencmd measure_temp
        # Set CPU governor to conservative
        echo "conservative" | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
        ```

   - Performance Optimization:
     1. Update GPU memory split:
        ```bash
        # Edit config
        sudo nano /boot/config.txt
        # Add or modify the line
        gpu_mem=16
        ```
     
     2. Enable overclocking (use cautiously):
        ```bash
        # Add to /boot/config.txt
        over_voltage=2
        arm_freq=1750
        ```

   - Monitor Mining Status:
     ```bash
     # View real-time hash rate
     watch -n 1 "cat /proc/cpuinfo | grep MHz"
     # Monitor system resources
     htop
     ```

6. **Run the Application**:
   - Start the application:
     ```bash
     python3 src/main.py
     ```

---

## Development Environment Setup
### Required Development Tools
```bash
# Install development tools
sudo apt install git python3-venv python3-dev build-essential
```

### Python Virtual Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

---

## System Specification Tools

### Required Software Tools
```bash
# Install essential monitoring tools
sudo apt install neofetch htop lm-sensors hardinfo
```

### 1. Basic System Info (using neofetch)
```bash
neofetch
```
Shows:
- OS version
- Kernel version
- CPU model
- RAM usage
- Disk usage
- GPU info

### 2. Hardware Details (using hardinfo)
```bash
hardinfo
```
Provides detailed reports on:
- CPU specifications
- Memory modules
- Storage devices
- Network adapters
- USB devices

### 3. Temperature Monitoring
```bash
# Initialize sensors
sudo sensors-detect
# View temperatures
sensors
```

### 4. Real-time Performance Monitor
```bash
htop
```
Displays:
- CPU usage per core
- Memory usage
- Running processes
- Load average

### 5. GPU Memory Split Check
```bash
vcgencmd get_mem gpu
```

### 6. CPU Frequency Monitor
```bash
watch -n1 vcgencmd measure_clock arm
```

These tools will help you assess if your Raspberry Pi meets the minimum requirements for mining operations. Install them before setting up the mining software.

---

## Security Considerations
### Basic Security Setup
```bash
# Update SSH configuration
sudo nano /etc/ssh/sshd_config
# Modify these lines:
PermitRootLogin no
PasswordAuthentication no
Port 2222  # Change default SSH port
```

### Firewall Configuration
```bash
# Install and configure UFW
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw allow 2222/tcp  # SSH
sudo ufw allow 5000/tcp  # Web interface
sudo ufw enable
```

---

## Monitoring and Alerts
### Automated Monitoring Script
```python
# monitor.py
import psutil
import time
import smtplib
from email.message import EmailMessage

def check_system():
    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    
    return {
        'temperature': cpu_temp,
        'cpu_usage': cpu_usage,
        'memory': memory
    }

def send_alert(message):
    # Configure email settings
    email_address = "your_email@example.com"
    email_password = "your_app_password"
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Mining Alert!'
    msg['From'] = email_address
    msg['To'] = email_address
    
    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
```

---

## Backup and Recovery
### Automated Backup Script
```bash
#!/bin/bash
# backup_config.sh
BACKUP_DIR="/home/pi/backups"
CONFIG_DIR="/home/pi/crypto-mining-assistant/config"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf $BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz $CONFIG_DIR

# Keep only last 5 backups
ls -t $BACKUP_DIR/config_backup_* | tail -n +6 | xargs -r rm
```

---

## Performance Tuning
### CPU Governor Settings
```bash
# Set performance governor
echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Monitor CPU frequency
watch -n 1 cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq
```

### Memory Management
```bash
# Add to /etc/sysctl.conf
vm.swappiness=10
vm.vfs_cache_pressure=50
```

---

## Logging System
### Log Rotation Configuration
```bash
# /etc/logrotate.d/crypto-mining
/home/pi/crypto-mining-assistant/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 640 pi pi
    sharedscripts
    postrotate
        systemctl restart crypto-mining
    endscript
}
```

---

## Testing Framework
### Unit Test Structure
```python
# tests/test_miner.py
import unittest
from src.mining.miner import MiningController

class TestMiningController(unittest.TestCase):
    def setUp(self):
        self.controller = MiningController()
    
    def test_start_mining(self):
        result = self.controller.start_mining()
        self.assertTrue(result)
        self.assertTrue(self.controller.is_mining)
    
    def test_stop_mining(self):
        self.controller.start_mining()
        result = self.controller.stop_mining()
        self.assertTrue(result)
        self.assertFalse(self.controller.is_mining)
```

---

## Documentation
### API Documentation Template
```python
"""
Mining Controller API Documentation

Endpoints:
GET /api/v1/status
    Returns current mining status
    Response: {
        "status": "active"|"inactive",
        "hashrate": float,
        "uptime": int
    }

POST /api/v1/control
    Control mining operations
    Body: {
        "action": "start"|"stop",
        "params": {
            "threads": int,
            "priority": int
        }
    }
"""
```

---

## User Interface Features
### Web Dashboard
- Access mining controls through a web browser at `http://raspberry-pi-ip:5000`
- Easy-to-use interface with:
  - Start/Stop mining buttons
  - Real-time mining statistics
  - Temperature and performance graphs
  - Wallet balance checker
  - Mining pool selector
  - Configuration editor

### Additional Requirements
```bash
pip3 install flask flask-socketio psutil plotly
```

### Dashboard Features
1. **Mining Control Panel**
   - One-click mining start/stop
   - Dropdown menu for selecting cryptocurrencies
   - Visual indicators for mining status

2. **System Monitoring**
   - Real-time temperature gauge
   - CPU usage graphs
   - Memory usage display
   - Network hashrate monitor

3. **Configuration Interface**
   - User-friendly forms for:
     - Wallet address input
     - Mining pool selection
     - Thread count adjustment
     - Performance settings

4. **Mobile Responsive Design**
   - Access dashboard from any device
   - Touch-friendly controls
   - Push notifications for important events

### Sample Dashboard Layout
```text
+----------------------------------+
|           MINING STATUS          |
|  [START]        [STOP]          |
|  Status: Active                  |
|  Hashrate: 245 H/s              |
+----------------------------------+
|         SYSTEM METRICS           |
|  Temperature: 65°C [||||||||  ]  |
|  CPU Usage: 85%   [||||||||| ]  |
|  Memory: 1.2GB    [||||||||  ]  |
+----------------------------------+
|      MINING CONFIGURATION        |
|  Pool: [Select Pool     ▼]      |
|  Wallet: [Input Address    ]    |
|  Threads: [3  ▼]              |
+----------------------------------+
```

### Security Features
- Password protection for dashboard
- SSL encryption support
- IP whitelist capability
- Session management

This user interface makes crypto mining more accessible to beginners while still providing advanced options for experienced users. The dashboard can be accessed from any device on your local network.

---

## Project Structure
```
crypto-mining-assistant/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── mining/
│   │   ├── __init__.py
│   │   └── miner.py
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── system_monitor.py
│   └── web/
│       ├── __init__.py
│       ├── routes.py
│       └── templates/
├── tests/
├── logs/
├── config/
├── requirements.txt
└── README.md
```

---

## Deployment Guide
### Systemd Service Setup
```bash
# Create service file
sudo nano /etc/systemd/system/crypto-miner.service

# Add content:
[Unit]
Description=Crypto Mining Assistant
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/crypto-mining-assistant
ExecStart=/home/pi/crypto-mining-assistant/venv/bin/python3 src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Cryptocurrency Selection Guide
### Recommended for Raspberry Pi
1. **Monero (XMR)**
   - CPU-friendly algorithm
   - Active community
   - Stable network

2. **Duino-Coin (DUCO)**
   - Designed for low-power devices
   - Quick rewards
   - Simple setup

3. **Dogecoin (DOGE)**
   - Lower difficulty
   - Active mining pools
   - Good for beginners

### Hardware-Specific Hashrates
```text
Typical Expected Performance:
RPi 4 (4GB):
- Monero: 2-5 H/s
- Duino-Coin: 800-1200 H/s
- Dogecoin: 0.2-0.5 MH/s

RPi 3 (1GB):
- Monero: 1-2 H/s
- Duino-Coin: 400-600 H/s
- Dogecoin: 0.1-0.2 MH/s
```

---

## Community and Support
- GitHub Issues: [Project Issues Page]
- Discord Server: [Community Chat]
- Documentation Wiki: [Project Wiki]
- Support Email: support@example.com

---

## License
```text
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Detailed Requirements & Challenges

### Minimum Hardware Requirements
1. **Raspberry Pi Specifications**:
   - Raspberry Pi 4 Model B (2GB RAM minimum, 4GB recommended)
   - CPU: 1.5GHz quad-core ARM Cortex-A72
   - Storage: 32GB Class 10 microSD card
   - Power Supply: 5V/3A USB-C power supply
   - Active cooling solution (fan or heatsink mandatory)

2. **Network Requirements**:
   - Stable internet connection (minimum 5 Mbps)
   - Ethernet connection recommended
   - Static IP address recommended

3. **Power Considerations**:
   - Continuous power draw: 5-7W idle, 15W under load
   - UPS recommended for stability
   - Monthly power consumption: ~10.8 kWh

### Technical Challenges

1. **Hardware Limitations**:
   - Low hash rates (2-5 H/s for Monero)
   - Limited CPU power compared to ASICs
   - Temperature management issues
   - Storage wear due to continuous operation

2. **Software Challenges**:
   - Limited mining software options for ARM architecture
   - Potential OS stability issues under prolonged load
   - Regular updates needed for security
   - Pool compatibility issues

3. **Performance Bottlenecks**:
   ```text
   Typical Performance Metrics:
   - Hash Rate: 2-5 H/s (Monero)
   - Power Efficiency: ~0.3 H/W
   - Temperature Range: 65-80°C
   - Network Latency Impact: ~5-10%
   ```

4. **Economic Challenges**:
   - Low profitability (often negative ROI)
   - High power consumption relative to mining reward
   - Network difficulty increases over time
   - Cryptocurrency price volatility

### Mitigation Strategies

1. **Temperature Management**:
   ```bash
   # Install temperature monitoring
   sudo apt install lm-sensors
   # Set up automatic fan control
   sudo nano /etc/rc.local
   # Add before exit 0:
   /usr/bin/python3 /home/pi/fan_control.py &
   ```

2. **Performance Optimization**:
   - Use lightweight OS distribution
   - Disable unnecessary services
   - Optimize memory usage
   - Configure swap space:
   ```bash
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Set CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

3. **Network Optimization**:
   ```bash
   # Set static IP
   sudo nano /etc/dhcpcd.conf
   # Add:
   interface eth0
   static ip_address=192.168.1.XX/24
   static routers=192.168.1.1
   static domain_name_servers=1.1.1.1
   ```

### Success Metrics
1. **Stability Indicators**:
   - Uptime > 99%
   - Temperature < 75°C
   - CPU throttling < 5%
   - Network connectivity > 99%

2. **Performance Targets**:
   - Consistent hash rate
   - < 1% rejected shares
   - < 100ms pool latency
   - Zero hardware errors

---

## Future Enhancements
- Add support for GPU mining.
- Integrate advanced monitoring tools.
- Provide mobile app support for remote management.

---

## Notes
- Cryptocurrency mining on a Raspberry Pi is not highly profitable due to its limited processing power. This app is intended for educational purposes or small-scale mining experiments.
- Ensure proper cooling for your Raspberry Pi to avoid overheating during mining operations.

---

## Disclaimer
Cryptocurrency mining consumes significant power and may not be profitable depending on the hardware and electricity costs. Use this application responsibly and at your own risk.