from flask import Flask, request, send_file, jsonify
import pyautogui
from PIL import ImageGrab
import io
import socket
import requests
import psutil
import subprocess

app = Flask(__name__)

@app.route('/mouse-position', methods=['POST'])
def mouse_position():
    data = request.json
    x, y = data['x'], data['y']
    
    # Move the mouse to the given position
    pyautogui.moveTo(x, y)
    
    # Capture a screenshot
    screenshot = ImageGrab.grab()
    
    # Save the screenshot to a bytes buffer
    buffer = io.BytesIO()
    screenshot.save(buffer, format='PNG')
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png')

@app.route('/execute-command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command', '')
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        # Execute the command and get the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
        
        if error:
            output += f"\nError: {error}"
        
        return jsonify({'output': output}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 80))  # Connect to Google's public DNS
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def get_network_info():
    addrs = psutil.net_if_addrs()
    info = {}
    for interface, addresses in addrs.items():
        info[interface] = [addr.address for addr in addresses if addr.family == psutil.AF_INET]
    return info

def get_hostname():
    return socket.gethostname()

if __name__ == '__main__':
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    port = 5000  # Port number for the Flask server
    hostname = get_hostname()
    network_info = get_network_info()

    print(f"Hostname: {hostname}")
    print(f"Local IP address: {local_ip}:{port}")
    print(f"Public IP address: {public_ip}")
    print("Network Interfaces:")
    for iface, ips in network_info.items():
        print(f"  {iface}: {', '.join(ips)}")
    
    app.run(host='0.0.0.0', port=port)
