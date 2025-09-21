# https://www.reddit.com/r/wiz/comments/1582jfx/guide_to_controlling_a_wiz_lightplug_via_windows/
# https://seanmcnally.net/wiz-config.html

from flask import Flask, render_template, request, jsonify
from flask.views import MethodView
import subprocess
import os

app = Flask(__name__)

# Lightbulb's IP address
BULB_IP = "192.168.1.18"
PORT = "38899"

log_path = "logs.txt"

if os.path.exists(log_path) == False:
    with open(log_path,'w') as file:
        file.write()
else:
    pass

class CommandClass:
    def __init__(self,command):
        self.command = command
        
    def get_and_store_command(self):
        self.command_str = f'echo {self.command} | ncat -u -w 1 {BULB_IP} {PORT}'
        with open(log_path,'a') as file:
            file.write(self.command_str + '\n')
        return self.command_str

    def send_command(self):
        # Ensure proper escaping
        result = subprocess.run(self.command_str, shell=True, capture_output=True, text=True)
        print(f"Sent command: {self.command_str}")  # Debugging
        print(f"Output: {result.stdout}")  # Debugging
        return result.stdout

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
