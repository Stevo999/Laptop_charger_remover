import platform
import subprocess

def get_laptop_info():
    laptop_info = {}

    if platform.system() == "Linux":
        result = subprocess.run(["dmidecode", "-s", "system-manufacturer"], capture_output=True, text=True)
        laptop_info["Manufacturer"] = result.stdout.strip()

        result = subprocess.run(["dmidecode", "-s", "system-product-name"], capture_output=True, text=True)
        laptop_info["Model"] = result.stdout.strip()
    elif platform.system() == "Windows":
        result = subprocess.run(["wmic", "csproduct", "get", "vendor"], capture_output=True, text=True)
        laptop_info["Manufacturer"] = result.stdout.strip().split("\n")[1].strip()

        result = subprocess.run(["wmic", "csproduct", "get", "name"], capture_output=True, text=True)
        laptop_info["Model"] = result.stdout.strip().split("\n")[1].strip()

    return laptop_info

# Get the operating system information
os_name = platform.system()
os_version = platform.release()

# Get the laptop information
laptop_info = get_laptop_info()

# Print the laptop information
print("Laptop Information:")
print(f"Operating System: {os_name} {os_version}")
print(f"Manufacturer: {laptop_info.get('Manufacturer', 'N/A')}")
print(f"Model: {laptop_info.get('Model', 'N/A')}")

