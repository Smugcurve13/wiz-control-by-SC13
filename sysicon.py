import pystray
from PIL import Image, ImageDraw
from flask import Flask
import threading
import time

app = Flask(__name__)

# Function to create an icon image
def create_icon(status):
    img = Image.new('RGB', (64, 64), color='green' if status else 'red')
    d = ImageDraw.Draw(img)
    d.ellipse((10, 10, 54, 54), fill='green' if status else 'red')
    return img

# Function to start the Flask app in a separate thread
def start_app():
    app.run(port=5000)

# Function to start or stop the app with the tray icon
def setup_icon():
    status = False
    icon = pystray.Icon("WiZ Light Control")
    
    def on_start(icon, item):
        nonlocal status
        if not status:
            threading.Thread(target=start_app, daemon=True).start()
            status = True
            icon.icon = create_icon(status)
    
    def on_stop(icon, item):
        nonlocal status
        # Add logic to stop your app if needed, like terminating the Flask app gracefully
        status = False
        icon.icon = create_icon(status)

    icon.icon = create_icon(status)
    icon.menu = pystray.Menu(
        pystray.MenuItem("Start WiZ Control", on_start),
        pystray.MenuItem("Stop WiZ Control", on_stop),
        pystray.MenuItem("Quit", lambda icon: icon.stop())
    )
    icon.run()

# Starting the icon setup
setup_icon()
