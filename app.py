# https://www.reddit.com/r/wiz/comments/1582jfx/guide_to_controlling_a_wiz_lightplug_via_windows/
# https://seanmcnally.net/wiz-config.html

from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# Lightbulb's IP address
BULB_IP = "192.168.1.4"
PORT = "38899"

def send_command(command):
    # Ensure proper escaping
    command_str = f'echo {command} | ncat -u -w 1 {BULB_IP} {PORT}'
    result = subprocess.run(command_str, shell=True, capture_output=True, text=True)
    print(f"Sent command: {command_str}")  # Debugging
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
    response = send_command(command)
    print(f"Response: {response}")  # Debugging
    return jsonify({"response": response})

@app.route('/control', methods=['POST'])
def control_light():
    command = request.json['command']
    log_command_to_db(command)  # Log command in a database
    # Send the command to the light device
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
