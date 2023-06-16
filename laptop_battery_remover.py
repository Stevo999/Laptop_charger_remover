import time
import platform
import subprocess

def get_battery_info():
    if platform.system() == "Linux":
        result = subprocess.run(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"], capture_output=True, text=True)
        output = result.stdout.strip()
        return output
    elif platform.system() == "Windows":
        result = subprocess.run(["WMIC", "Path", "Win32_Battery", "Get", "BatteryStatus"], capture_output=True, text=True)
        output = result.stdout.strip()
        return output

def unplug_charger():
    battery_info = get_battery_info()
    print("Battery info:", battery_info)

    if "state:\t\tcharged" in battery_info:
        print("Battery is fully charged. Unplugging the charger...")
        if platform.system() == "Linux":
            subprocess.run(["echo", "0", "|", "sudo", "tee", "/sys/class/power_supply/AC/online"])
        elif platform.system() == "Windows":
            subprocess.run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_NONE", "PERCENTCRIT", "80"])
    elif "state:\t\tdischarging" in battery_info:
        battery_percent = int(battery_info.split("percentage:\t")[1].split("%")[0])
        if battery_percent < 20:
            print("Battery level is low. Plugging in the charger...")
            if platform.system() == "Linux":
                subprocess.run(["echo", "1", "|", "sudo", "tee", "/sys/class/power_supply/AC/online"])
            elif platform.system() == "Windows":
                subprocess.run(["powercfg", "/setacvalueindex", "SCHEME_CURRENT", "SUB_NONE", "PERCENTCRIT", "20"])

while True:
    unplug_charger()
    time.sleep(60)  # Check the battery status every minute

