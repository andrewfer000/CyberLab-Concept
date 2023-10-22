import random
def generate_random_mac():
    fixed_parts = ["52", "54", "00"]
    random_parts = [f'{random.randint(0, 99):02x}' for _ in range(3)]
    mac_address = ":".join(fixed_parts + random_parts)
    return mac_address

def generate_random_ip():
    x_parts = [random.randint(1, 255) for _ in range(3)]
    return f"10.{x_parts[1]}.{x_parts[2]}"

def replace_ip_pattern(base_ip, machine_ip):
    machine = int(machine_ip.split('.')[-1])
    full_ip = f"{base_ip}.{machine}"
    return full_ip
