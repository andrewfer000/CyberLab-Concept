from pssh.clients import ParallelSSHClient
import hashlib

def LinuxFileChecker(host, username, password, filepath):
    hosts = [f'{host}']
    user = f'{username}'
    password = f'{password}'
    command = f'ls {filepath}'

    client = ParallelSSHClient(hosts, user=user, password=password)
    output = client.run_command(command)

    for host, host_output in output.items():
        if host_output.exit_code == 0:
            print(f"File exists on {host}: {host_output.stdout}")
        else:
            print(f"Error on {host}: {host_output.stderr}")

    client.close()

def calculate_remote_sha256(host, user, password, file_path):
    client = ParallelSSHClient(host, user=user, password=password)
    sha256_hashes = {}

    try:
        output = client.run_command(f'sha256sum {file_path}')
        if host_output.exit_code == 0:
            sha256_hash = host_output.stdout.strip().split()[0]
            sha256_hashes[host] = sha256_hash
        else:
            sha256_hashes[host] = f"Error: {host_output.stderr.strip()}"
    except Exception as e:
        sha256_hashes['error'] = f"Error: {e}"
    finally:
        client.close()

    return sha256_hashes
