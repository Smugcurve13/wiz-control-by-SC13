import tkinter as tk
import requests


class WiZLightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiZ Light Control")

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Power controls
        frame_power = tk.Frame(self.root, padx=10, pady=10)
        frame_power.pack()

        tk.Button(frame_power, text="Turn On", command=self.turn_on).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_power, text="Turn Off", command=self.turn_off).pack(side=tk.LEFT, padx=5)

        # Brightness slider
        frame_brightness = tk.Frame(self.root, padx=10, pady=10)
        frame_brightness.pack()

        tk.Label(frame_brightness, text="Brightness").pack(side=tk.LEFT, padx=5)
        self.brightness_slider = tk.Scale(frame_brightness, from_=0, to=100, orient=tk.HORIZONTAL)
        self.brightness_slider.set(50)  # Default value
        self.brightness_slider.pack(side=tk.LEFT, padx=5)
        self.brightness_slider.bind("<B1-Motion>", self.on_brightness_change)
        self.brightness_slider.bind("<ButtonRelease-1>", self.on_brightness_release)

        # Temperature slider
        frame_temperature = tk.Frame(self.root, padx=10, pady=10)
        frame_temperature.pack()

        tk.Label(frame_temperature, text="Temperature (K)").pack(side=tk.LEFT, padx=5)
        self.temperature_slider = tk.Scale(frame_temperature, from_=2700, to=6500, orient=tk.HORIZONTAL)
        self.temperature_slider.set(4000)  # Default value
        self.temperature_slider.pack(side=tk.LEFT, padx=5)
        self.temperature_slider.bind("<B1-Motion>", self.on_temperature_change)
        self.temperature_slider.bind("<ButtonRelease-1>", self.on_temperature_release)

        # RGB Color picker
        frame_color = tk.Frame(self.root, padx=10, pady=10)
        frame_color.pack()

        tk.Label(frame_color, text="RGB Color").pack(side=tk.LEFT, padx=5)
        self.color_picker = tk.StringVar()
        self.color_entry = tk.Entry(frame_color, textvariable=self.color_picker)
        self.color_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_color, text="Set Color", command=self.set_color).pack(side=tk.LEFT, padx=5)

        # Initialize throttling variables
        self.throttling = False
        self.throttle_delay = 200  # milliseconds

    def send_command(self, command):
        try:
            response = requests.post("http://localhost:5000/control", json={"command": command})
            response.raise_for_status()  # Raise error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {"error": str(e)}

    def throttled_command(self, command):
        if not self.throttling:
            self.send_command(command)
            self.throttling = True
            self.root.after(self.throttle_delay, self.release_throttle)

    def release_throttle(self):
        self.throttling = False

    def turn_on(self):
        command = '{"method":"setPilot","params":{"state":true}}'
        self.throttled_command(command)

    def turn_off(self):
        command = '{"method":"setPilot","params":{"state":false}}'
        self.throttled_command(command)

    def update_brightness(self, value):
        command = f'{{"method":"setPilot","params":{{"dimming":{value}}}}}'
        self.throttled_command(command)

    def on_brightness_change(self, event):
        # Handle real-time changes (if needed)
        pass

    def on_brightness_release(self, event):
        value = self.brightness_slider.get()
        self.update_brightness(value)

    def update_temperature(self, value):
        command = f'{{"method":"setPilot","params":{{"temp":{value}}}}}'
        self.throttled_command(command)

    def on_temperature_change(self, event):
        # Handle real-time changes (if needed)
        pass

    def on_temperature_release(self, event):
        value = self.temperature_slider.get()
        self.update_temperature(value)

    def set_color(self):
        hex_color = self.color_picker.get()
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        command = f'{{"method":"setPilot","params":{{"r":{r},"g":{g},"b":{b}}}}}'
        self.throttled_command(command)


def main():
    root = tk.Tk()
    app = WiZLightApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
