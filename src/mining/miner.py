import subprocess
import json
from datetime import datetime
import os
import signal
import sys
import platform

class MiningManager:
    def __init__(self):
        self.current_process = None
        self.mining_status = {
            'is_mining': False,
            'start_time': None,
            'hashrate': 0,
            'shares_found': 0,
            'pool': '',
            'wallet': '',
            'coin': 'DOGE'
        }
        self.default_pool = 'stratum+tcp://pool.systm.org:22550'
        # Set up miner executable path
        self.miner_path = self._get_miner_path()

    def _get_miner_path(self):
        """Get the appropriate miner executable path based on OS"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if platform.system() == 'Windows':
            return os.path.join(base_dir, 'miners', 'cpuminer-multi', 'cpuminer-gw64-core2.exe')
        return 'cpuminer'  # For Linux/Unix systems

    def start_mining(self, config):
        if not self.mining_status['is_mining']:
            try:
                pool_url = config.get('pool_url', self.default_pool)
                wallet_address = config.get('wallet_address', '')
                
                if not wallet_address:
                    return {'status': 'error', 'message': 'Wallet address is required'}

                # Check if miner exists
                if not os.path.exists(self.miner_path):
                    return {'status': 'error', 'message': 'Mining software not found. Please install cpuminer-multi.'}

                # Create cpuminer command for Dogecoin
                command = [
                    self.miner_path,
                    '-a', 'scrypt',  # Algorithm for Dogecoin
                    '-o', pool_url,
                    '-u', wallet_address,
                    '-p', 'x',
                    '--threads=2'  # Adjust based on your CPU
                ]

                # Start the mining process
                self.current_process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == 'Windows' else 0
                )

                self.mining_status.update({
                    'is_mining': True,
                    'start_time': datetime.now().isoformat(),
                    'pool': pool_url,
                    'wallet': wallet_address
                })
                return {'status': 'success', 'message': 'Dogecoin mining started successfully'}
            except Exception as e:
                return {'status': 'error', 'message': f'Failed to start mining: {str(e)}'}
        return {'status': 'error', 'message': 'Mining is already running'}

    def stop_mining(self):
        if self.mining_status['is_mining']:
            try:
                if self.current_process:
                    if platform.system() == 'Windows':
                        # On Windows, we need to use taskkill to terminate the process tree
                        subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.current_process.pid)])
                    else:
                        os.kill(self.current_process.pid, signal.SIGTERM)
                    self.current_process = None
                
                self.mining_status.update({
                    'is_mining': False,
                    'start_time': None,
                    'hashrate': 0,
                    'shares_found': 0
                })
                return {'status': 'success', 'message': 'Mining stopped successfully'}
            except Exception as e:
                return {'status': 'error', 'message': f'Failed to stop mining: {str(e)}'}
        return {'status': 'error', 'message': 'Mining is not running'}

    def get_status(self):
        if self.current_process and self.mining_status['is_mining']:
            # Update hashrate and shares from miner output if available
            try:
                output = self.current_process.stdout.readline()
                if 'accepted' in output.lower():
                    self.mining_status['shares_found'] += 1
                if 'mh/s' in output.lower():
                    # Extract hashrate from miner output
                    for part in output.split():
                        if 'mh/s' in part.lower():
                            try:
                                self.mining_status['hashrate'] = float(part.split('mh')[0])
                            except ValueError:
                                pass
            except:
                pass
        return self.mining_status