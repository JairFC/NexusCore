import asyncio
import ipaddress
import platform

async def ping_host(ip: str) -> bool:
    system = platform.system().lower()
    count = "1"
    command = ["ping", "-n" if system == "windows" else "-c", count, ip]
    
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await proc.communicate()
    return proc.returncode == 0

async def scan_network(network: str):
    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError:
        return {"error": "Red inválida"}

    tasks = []
    for ip in net.hosts():
        tasks.append(ping_host(str(ip)))
    
    results = await asyncio.gather(*tasks)
    scanned = list(net.hosts())
    conectados = [str(ip) for ip, alive in zip(scanned, results) if alive]
    desconectados = [str(ip) for ip, alive in zip(scanned, results) if not alive]

    return {
        "conectados": conectados,
        "desconectados": desconectados
    }
