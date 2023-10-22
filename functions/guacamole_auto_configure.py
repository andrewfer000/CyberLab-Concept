import requests
import json
import random
import string
from functions.get_client_urls import get_client_url

def generate_authToken(input_username, input_password, GUACAMOLE_API_URL):
    auth_data = {
        "username": input_username,
        "password": input_password,
    }

    auth_response = requests.post(f"{GUACAMOLE_API_URL}/tokens", data=auth_data)

    if auth_response.status_code == 200:
        token = auth_response.text
        response_string = f"{token}"
        data = json.loads(response_string)
        auth_token = data.get('authToken')
    else:
        print(f"An Error has occured: {auth_response.status_code}")

    return auth_token

# Function to create a Guacamole user
def create_guacamole_user(auth_token, GUACAMOLE_API_URL):

    username = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    user_data = {
        "username": username,
        "password": password,
        "attributes": {
            "disabled": "",
            "expired": "",
            "access-window-start": "",
            "access-window-end": "",
            "valid-from": "",
            "valid-until": "",
            "timezone": "null",
            "guac-full-name": "",
            "guac-organization": "",
            "guac-organizational-role": ""
        }
    }

    response = requests.post(f"{GUACAMOLE_API_URL}/session/data/mysql/users?token={auth_token}", json=user_data)

    if response.status_code == 200:
        user_credentials = {
            "username": username,
            "password": password
        }
        return user_credentials
    else:
        return None

# Function to delete the guacamole user
def delete_guacamole_user(auth_token, username, GUACAMOLE_API_URL):
    response = requests.delete(f"{GUACAMOLE_API_URL}/session/data/mysql/users/{username}?token={auth_token}")

    if response.status_code == 204:
        return None
    else:
        print(f"ERROR: User delete fail {response.status_code}")
        return None

# Function to create guacamole connections
def create_guacamole_connections(auth_token, name, port, sftp, GUACAMOLE_API_URL):
    connection_data = {
            "parentIdentifier": "ROOT",
            "name": f"{name}",
            "protocol": "vnc",
            "parameters": {
                "port": f"{port}",
                "read-only": "",
                "swap-red-blue": "",
                "cursor": "",
                "color-depth": "",
                "clipboard-encoding": "",
                "disable-copy": "",
                "disable-paste": "",
                "dest-port": "",
                "recording-exclude-output": "",
                "recording-exclude-mouse": "",
                "recording-include-keys": "",
                "create-recording-path": "",
                "enable-sftp": f"{sftp}",
                "sftp-port": "",
                "sftp-server-alive-interval": "",
                "enable-audio": "",
                "audio-servername": "",
                "sftp-directory": "",
                "sftp-root-directory": "",
                "sftp-passphrase": "",
                "sftp-private-key": "",
                "sftp-username": "",
                "sftp-password": "",
                "sftp-host-key": "",
                "sftp-hostname": "",
                "recording-name": "",
                "recording-path": "",
                "dest-host": "",
                "password": "",
                "username": "",
                "hostname": "localhost"
            },
            "attributes": {
                "max-connections": "2",
                "max-connections-per-user": "2",
                "weight": "",
                "failover-only": "",
                "guacd-port": "",
                "guacd-encryption": "",
                "guacd-hostname": ""
            }
        }

    response = requests.post(f"{GUACAMOLE_API_URL}/session/data/mysql/connections?token={auth_token}", json=connection_data)
    if response.status_code != 200:
        print(f"Connection Creation Failed: {response.status_code}")
        print(response.content)
        return None
    else:
        connection_id = response.json().get("identifier")
        if connection_id:
            return connection_id
        else:
            print(f"Failed to retrieve connection identifier for: {connection_data.get('name')}")
            return None

# Process connection data
def connection_data(connections, auth_token, GUACAMOLE_API_URL):
    connection_data_list = []
    connection_ids_list = []

    for VM, connection in connections.items():
        name, port, sftp = connection
        connection_info, connection_id = create_guacamole_connections(auth_token, name, port, sftp)
        connection_data_list.append(connection_info)
        connection_ids_list.append(connection_id)

    return  connection_data_list, connection_ids_list

# Set the connection's permission
def set_user_permissions(username, connection_id, auth_token, GUACAMOLE_API_URL):
    api_url = f"{GUACAMOLE_API_URL}/session/data/mysql/users/{username}/permissions?token={auth_token}"

    patch_operations = [
        {
            "op": "add",
            "path": f"/connectionPermissions/{connection_id}",
            "value": "READ"
        }
    ]

    response = requests.patch(api_url, json=patch_operations)

    if response.status_code == 204:
        pass
    else:
        print(f"Failed to update permissions. Status code: {response.status_code}")

#Revoke Guacamole permissions
def revoke_user_permissions(username, connection_id, auth_token, GUACAMOLE_API_URL):
    api_url = f"{GUACAMOLE_API_URL}/session/data/mysql/users/{username}/permissions?token={auth_token}"

    patch_operations = [
        {
            "op": "remove",
            "path": f"/connectionPermissions/{connection_id}",
            "value": "READ"
        }
    ]

    response = requests.patch(api_url, json=patch_operations)

    if response.status_code == 204:
        pass
    else:
        print(f"Failed to update permissions. Status code: {response.status_code}")


# Delete Guacamole Connections
def delete_guacamole_connections(auth_token, connection_id, GUACAMOLE_API_URL):
    response = requests.delete(f"{GUACAMOLE_API_URL}/session/data/mysql/connections/{connection_id}?token={auth_token}")

    if response.status_code != 204:
        print(f"ERROR: Connection was not deleted: {response.status_code}")
        return None
    else:
        return None

#-----------------------------------------------------------------------------------------------





