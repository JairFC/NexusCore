import subprocess

def realizar_ping(ip):
    try:
        output = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL)
        return output.returncode == 0
    except Exception as e:
        return False
