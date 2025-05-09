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

    all_hosts = list(net.hosts())

    if len(all_hosts) < 3:
        return {"conectados": [], "desconectados": []}

    gateway_ip = str(all_hosts[0])  # .1
    restante_hosts = [str(ip) for ip in all_hosts[1:]]  # incluye .254, excluye .255 automáticamente

    total_ips = [gateway_ip] + restante_hosts

    tasks = [ping_host(ip) for ip in total_ips]
    results = await asyncio.gather(*tasks)

    conectados = []
    desconectados = []

    for ip, alive in zip(total_ips, results):
        if ip == gateway_ip:
            continue  # verificar sin mostrar
        if alive:
            conectados.append(ip)
        else:
            desconectados.append(ip)

    return {
        "conectados": conectados,
        "desconectados": desconectados
    }
