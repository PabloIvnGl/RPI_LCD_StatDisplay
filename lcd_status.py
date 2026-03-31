import time
import subprocess
from rpi_lcd import LCD

# Inicializa LCD (I2C 16x2)
lcd = LCD()

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000.0
        return f"{temp:.1f}C"
    except:
        return "N/A"

def webui_status():
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "open-webui"],
            capture_output=True,
            text=True
        )
        return "ON" if result.stdout.strip() == "true" else "OFF"
    except:
        return "OFF"

def get_rpi_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error al obtener el IP: {e}")
        return "N/A"
        
def get_memory_usage():
    try:
        result = subprocess.run(
            ["free", "-m"],
            capture_output=True,
            text=True
        )
        memory_info = result.stdout.split("\n")[1].split()
        used_mem = int(memory_info[2])
        total_mem = int(memory_info[1])
        return f"{used_mem}/{total_mem}MB"
    except Exception as e:
        print(f"Error al obtener la memoria: {e}")
        return "N/A"
        

try:
    lcd.clear()
    while True:
        status = webui_status()
        temp = get_cpu_temp()
        rpi_ip = get_rpi_ip()
        memory_usage = get_memory_usage()

        line1 = f"WebUI IA: {status}"
        line2 = f"IP:{rpi_ip}"

        lcd.text(line1.ljust(16), 1)
        lcd.text(line2.ljust(16), 2)
        time.sleep(4)

        line1 = f"CPU: {temp}"
        line2 = f"RAM:{memory_usage}"
        lcd.text(line1.ljust(16), 1)
        lcd.text(line2.ljust(16), 2)
        time.sleep(4)
except KeyboardInterrupt:
    lcd.clear()
    lcd.text("Apagando...", 1)
    time.sleep(1)
    lcd.clear()
