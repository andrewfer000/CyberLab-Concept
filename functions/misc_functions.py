import random, json, random, string, os, argparse, shutil
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

def WriteSessionData(componet, indata, session_id):
    file_path = os.path.join(f"sessions/{session_id}", "session.json")

    with open(file_path, 'r') as file:
        data = json.load(file)

    if componet == "machine":
        data[session_id]['VMinfo'][indata.get("Machine_Name")] = {
            'isSuspended': False,
            'isOn': True,
            'Networks': indata.get("Networks"),
            'Disks': indata.get("Disks"),
            'CPUCores': indata.get("CPUCores"),
            'Memory': indata.get("Memory"),
            'VNC_Port': indata.get("VNC_Port"),
            'machine_data_ips': indata.get("machine_data_ips"),
            'machine_data_macs': indata.get("machine_data_macs")
        }

    elif componet == "network":
        data[session_id]['Networkinfo'][indata.get("Network_Name")] = {
            'isSuspended': False,
            'isOn': True,
            "Type": indata.get("Type"),
            "HostAddr": indata.get("HostAddr"),
            "Subnet": indata.get("Subnet"),
            "DHCPv4StartRange": indata.get("DHCPv4StartRange"),
            "DHCPv4EndRange": indata.get("DHCPv4EndRange"),
            "DHCPleases" : indata.get("DHCPleases")
        }

    elif componet == "guacamole":
        data[session_id]['Guacamole'] = {
            "Session_User": indata.get("Session_User"),
            "Session_Password": indata.get("Session_Password"),
            "Session_Auth_Token": indata.get("Session_Auth_Token"),
            "Session_Connection_Names": indata.get("Session_Connection_Names"),
            "Session_Client_URLs": indata.get("Session_Client_URLs")
        }

    elif componet == "InTextQuestion":
        data[session_id]['Questions'][indata.get("Question_id")] = {
            "Question_Type": indata.get("Question_Type"),
            "Question_Text": indata.get("Question_Text"),
            "Multiple_Choice_Options": indata.get("Multiple_Choice_Options"),
            "Answer": indata.get("Answer"),
            "Submitted": "null"

        }

    elif componet == "Checker":
        data[session_id]['Checkers'][indata.get("Checker_id")] = {
            "Checker_Type": indata.get("Checker_Type"),
            "Checker_Task": indata.get("Checker_Task"),
            "Checker_Condition": indata.get("Checker_Condition"),
            "Grade_Value": indata.get("Grade_Value"),
            "Submitted": "null"
        }

    else:
        print(f"ERROR: Componet: {componet} Does not Exist!")

    # Write the updated data back to data.json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
