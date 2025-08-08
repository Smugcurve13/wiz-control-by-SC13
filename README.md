# WiZ Light Control

A Python Flask web application for controlling WiZ smart lights and plugs via a user-friendly web interface.

![WiZ Control App](wiz%20app%20icon.png)

## Features

- 🌈 **Color Control**: Change light colors using an intuitive color picker
- 💡 **Brightness Control**: Adjust brightness with a slider
- 🔛 **Power Control**: Turn lights on/off with simple buttons
- 🌐 **Web Interface**: Control your lights from any device with a web browser
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🎨 **Beautiful UI**: Modern Bootstrap-based interface with gradient background
- 📋 **System Tray Integration**: Run the app in the background with system tray support

## Prerequisites

- Python 3.6 or higher
- WiZ smart lights/plugs connected to your local network
- Knowledge of your WiZ device's IP address

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Smugcurve13/wiz-control-by-SC13.git
   cd wiz-control-by-SC13
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your device IP**:
   Open `app.py` and update the `BULB_IP` variable with your WiZ device's IP address:
   ```python
   BULB_IP = "192.168.1.18"  # Replace with your device's IP
   ```

## Usage

### Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:5000`

3. **Control your lights**:
   - Use the color picker to change light colors
   - Adjust brightness with the slider
   - Turn lights on/off with the power buttons

### System Tray Mode

The application includes system tray functionality for running in the background:

```bash
python sysicon.py
```

This will minimize the app to your system tray, allowing you to access controls without keeping a browser window open.

## Project Structure

```
wiz-control-by-SC13/
├── app.py                 # Main Flask application
├── application.py         # Alternative application entry point
├── sysicon.py            # System tray integration
├── requirements.txt       # Python dependencies
├── logs.txt              # Application logs
├── templates/
│   └── index.html        # Web interface template
├── static/
│   ├── favicon.ico       # App icon
│   └── gradient.jpg      # Background image
└── README.md             # This file
```

## Dependencies

- **Flask**: Web framework for the application
- **requests**: HTTP library for communicating with WiZ devices
- **pystray**: System tray integration
- **Pillow**: Image processing for system tray icon
- **plyer**: Cross-platform notification system
- **beautifulsoup4**: HTML parsing utilities

## API Endpoints

The application provides REST API endpoints for controlling lights:

- `GET /`: Main web interface
- `POST /control`: Send commands to WiZ devices
- Additional endpoints for specific light functions

## Configuration

### Finding Your WiZ Device IP

1. Use your router's admin panel to find connected devices
2. Use network scanning tools like `nmap`:
   ```bash
   nmap -sn 192.168.1.0/24
   ```
3. Check the WiZ mobile app device settings

### Port Configuration

The default WiZ port `38899` is configured in the application. This is the standard port for WiZ device communication and typically doesn't need to be changed.

## Troubleshooting

### Common Issues

1. **Device not responding**: 
   - Verify the IP address is correct
   - Ensure the device is on the same network
   - Check that the WiZ device is powered on

2. **Web interface not loading**:
   - Ensure port 5000 is not blocked by firewall
   - Try accessing via `127.0.0.1:5000` instead of `localhost`

3. **Dependencies issues**:
   - Make sure all packages from `requirements.txt` are installed
   - Consider using a virtual environment

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## References

This project was inspired by and references:
- [Reddit Guide: Controlling WiZ lights via Windows](https://www.reddit.com/r/wiz/comments/1582jfx/guide_to_controlling_a_wiz_lightplug_via_windows/)
- [Sean McNally's WiZ Configuration Guide](https://seanmcnally.net/wiz-config.html)

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information about your problem

---

**Made with ❤️ by SC13**
