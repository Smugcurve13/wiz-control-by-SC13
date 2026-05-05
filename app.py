# https://www.reddit.com/r/wiz/comments/1582jfx/guide_to_controlling_a_wiz_lightplug_via_windows/
# https://seanmcnally.net/wiz-config.html

from flask import Flask, render_template, request, jsonify
from flask.views import MethodView
import subprocess
import os
import socket
import sys

app = Flask(__name__)

# Lightbulb's IP address
BULB_IP = "192.168.1.18"
PORT = "38899"

log_path = "logs2.txt"

if os.path.exists(log_path) == False:
    with open(log_path,'w') as file:
        file.write()
else:
    pass

# Detect OS and set the appropriate method
def get_os_type():
    """Detect the operating system."""
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    return 'unknown'

OS_TYPE = get_os_type()
print(f"Detected OS: {OS_TYPE}")  # Debugging

class CommandClass:
    def __init__(self,command):
        self.command = command
        
    def get_and_store_command(self):
        if OS_TYPE == 'windows':
            # Windows: use ncat (from nmap) - no -n needed
            self.command_str = f'echo {self.command} | ncat -u -w 1 {BULB_IP} {PORT}'
        else:
            # Linux/Mac: use netcat (nc) with -n to prevent newline
            self.command_str = f'echo -n "{self.command}" | nc -u -w 1 {BULB_IP} {PORT}'
        
        with open(log_path,'a') as file:
            file.write(self.command_str + '\n')
        return self.command_str

    def send_command(self):
        # Try Python socket method first (more reliable cross-platform)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            sock.sendto(self.command.encode(), (BULB_IP, int(PORT)))
            response = "Command sent via Python socket"
            sock.close()
            print(f"Sent command via socket: {self.command}")  # Debugging
        except Exception as e:
            # Fallback to subprocess method
            try:
                result = subprocess.run(self.command_str, shell=True, capture_output=True, text=True)
                response = result.stdout
                print(f"Sent command: {self.command_str}")  # Debugging
                print(f"Output: {result.stdout}")  # Debugging
            except Exception as e2:
                response = f"Error: {str(e2)}"
                print(f"Error: {e2}")  # Debugging
        
        return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    print(f"Received command: {command}")  # Debugging

    command_instance = CommandClass(command)
    command_instance.get_and_store_command()
    response = command_instance.send_command()
    print(f"Response: {response}")  # Debugging
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5002)
