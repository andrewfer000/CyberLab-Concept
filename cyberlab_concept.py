import json, random, string, os, argparse, shutil
from jinja2 import Environment, FileSystemLoader, Template
from datetime import datetime
from functions.libvirt_automated import *
from functions.guacamole_auto_configure import *
from functions.misc_functions import *
from functions.xml_generator import *
from functions.get_client_urls import get_client_url
from functions.generate_lab import GenerateLab

with open('config.json', 'r') as file:
    config = json.load(file)

GUAC_SECURITY = config['connections']['Local']['Guacamole']['Security']
GUACAMOLE_URL = config['connections']['Local']['Guacamole']['URL']
GUAC_FULL_URL = f"{GUAC_SECURITY}://{GUACAMOLE_URL}"
GUACAMOLE_API_URL = f"{GUAC_FULL_URL}/api"
GUACAMOLE_ADMIN_UNAME = config['connections']['Local']['Guacamole']['AdminUsername']
GUACAMOLE_ADMIN_PASS = config['connections']['Local']['Guacamole']['AdminPassword']
LIBVIRT_SECURITY = config['connections']['Local']['Libvirt']['Security']
LIBVIRT_URL = config['connections']['Local']['Libvirt']['URL']

def DestoryOnError():
    print("Work In Progress")
    return None

def CreateSession(machines, course, lab):
    current_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    string_length = 10
    session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=string_length))

    subdirectory_path = os.path.join("sessions", f"{session_id}")
    disks_path = os.path.join(subdirectory_path, "disks")
    os.makedirs(subdirectory_path)
    os.makedirs(disks_path)

    file_path = os.path.join(f"sessions/{session_id}", "session.json")
    session_data = {
        session_id: {
            "Metadata": {
                "User": "Unused",
                 "DateTimeCreated": current_datetime,
                 "CourseLab": f"{course}/{lab}",
                 "isSuspended": False
                },
            "VMinfo":{
                },
            "Networkinfo":{
                },
            "Guacamole":{
                },
            "Questions":{
                },
            "Checkers":{
                }
            }
        }

    with open(file_path, 'w') as json_file:
        json.dump(session_data, json_file, indent=4)
        json_file.close()


    vm_vnc_ports = []
    for machine_name, details in machines.items():
        vnc_port = random.randint(49155, 65510)
        vm_vnc_ports.append({f"{machine_name}": vnc_port})
    return session_id, vm_vnc_ports

# This Function creates tcomponethe VM envirtonment for the lab.
def CreateVM(machines, networks, vm_vnc_ports, session_id, course_dir):
    machineips = []
    machinemacs = []
    for network_name, network_info in networks.items():
        dhcp_leases = ""
        random_number = random.randint(1000, 9999)
        br_name = f"virbr{random_number}"
        mac_addr = generate_random_mac()
        base_ip = generate_random_ip()

        for assignment in network_info.get("ipassignments", []):
            net_machine_name = assignment[0]
            net_ip_address = assignment[1]

            full_ip = replace_ip_pattern(base_ip, net_ip_address)

            for machine_name, details in machines.items():
                for network in details.get("Network", []):
                    vm_mac = generate_random_mac()
                    nic_model = network[0]
                    vm_network_name = network[1]
                    if net_machine_name == machine_name:
                        machinemac = {machine_name: vm_mac}
                        machinemacs.append(machinemac)
                    if net_machine_name == machine_name and network_name == vm_network_name:
                        dhcp_lease_string = f"""
                        <host mac='{ vm_mac }' name='{ f"{vm_network_name}_{session_id}" }' ip='{ full_ip }'/>"""
                        dhcp_leases = dhcp_leases + dhcp_lease_string
                        machineip = {machine_name: full_ip}
                        machineips.append(machineip)
                else:
                    pass

        ip_addr = replace_ip_pattern(base_ip, network_info.get("HostAddr"))
        sub_mask = network_info.get("Subnet")

        if network_info.get("Type") == "private":
            bridge_conf = f"""
            <bridge name='{br_name}' stp='on' delay='0'/>
            <mac address='{mac_addr}'/>
            <ip address='{ip_addr}' netmask='{sub_mask}'>
            """
        elif network_info.get("Type") == "internet":
            bridge_conf = f"""
            <forward mode="nat"/>
            <bridge name='{br_name}' stp='on' delay='0'/>
            <mac address='{mac_addr}'/>
            <ip address='{ip_addr}' netmask='{sub_mask}'>
            """
        else:
            print("WARNING: Network not specified, Please check lab config. Destorying session")
            DestorySession(session_id)
            return None



        network_name = f"{network_name}_{session_id}"
        dhcp_start = replace_ip_pattern(base_ip, network_info.get("DHCPv4StartRange"))
        dhcp_end = replace_ip_pattern(base_ip, network_info.get("DHCPv4EndRange"))

        net_xml = generate_net_config(network_name, dhcp_start, dhcp_end, dhcp_leases, bridge_conf)
        create_internal_network(net_xml)

        network_data = {
            "Network_Name": network_name,
            "Type": network_info.get("Type"),
            "HostAddr": ip_addr,
            "Subnet": network_info.get("Subnet"),
            "DHCPv4StartRange": dhcp_start,
            "DHCPv4EndRange": dhcp_end,
            "DHCPleases" : dhcp_leases.replace('\n', ',').replace(' ' * 24, ' ')
            }

        WriteSessionData("network", network_data, session_id)


    for machine_name, details in machines.items():

        for machine_dict in vm_vnc_ports:
            if machine_name in machine_dict:
                vnc_port = machine_dict[machine_name]
            else:
                pass

        disk_conf = ""
        VM_Disks = []
        diski = 0
        driveletter = 'a'
        for disk in details.get("Disks", []):
            for disk_type, path in disk.items():
                if disk_type == "cdrom":
                    source_file_path = f"{course_dir}/vm_images/{path}"
                    destination_file_path = f"sessions/{session_id}/disks/{session_id}_{path}"
                    try:
                        with open(source_file_path, 'rb') as source_file:
                            file_content = source_file.read()

                        with open(destination_file_path, 'wb') as destination_file:
                            destination_file.write(file_content)
                    except Exception as e:
                        print(f'An error occurred: {e}')
                    abspath = os.path.abspath(destination_file_path)

                    disk_string = f""" <disk type="file" device="cdrom">
                    <driver name="qemu" type="raw"/>
                    <source file="{abspath}"/>
                    <target dev="sd{driveletter}" bus="sata"/>
                    <readonly/>
                    <address type="drive" controller="0" bus="0" target="0" unit="{diski}"/>
                 </disk>
                """
                    diski = diski + 1
                    driveletter = chr(ord(driveletter) + 1)

                elif disk_type == "lindisk":
                    source_file_path = f"{course_dir}/vm_images/{path}"
                    destination_file_path = f"sessions/{session_id}/disks/{session_id}_{machine_name}_{path}"
                    try:
                        shutil.copy2(source_file_path, destination_file_path)
                    except Exception as e:
                        print(f"Error: {e}. Option 2 Failed the Lab will not work")

                    abspath = os.path.abspath(destination_file_path)

                    disk_string = f""" <disk type='file' device='disk'>
                    <driver name='qemu' type='qcow2'/>
                    <source file='{abspath}'/>
                    <target dev='vda' bus='virtio'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                 </disk>
                """
                elif disk_type == "windisk":
                    source_file_path = f"{course_dir}/vm_images/{path}"
                    destination_file_path = f"sessions/{session_id}/disks/{session_id}_{machine_name}_{path}"
                    try:
                        shutil.copy2(source_file_path, destination_file_path)
                    except Exception as e:
                        print(f"Error: {e}. Option 2 Failed the Lab will not work")

                    abspath = os.path.abspath(destination_file_path)

                    disk_string = f""" <disk type='file' device='disk'>
                    <driver name='qemu' type='qcow2'/>
                    <source file='{abspath}'/>
                    <target dev="sd{driveletter}" bus="sata"/>
                    <address type="drive" controller="0" bus="0" target="0" unit="{diski}"/>
                </disk>
                """
                    diski = diski + 1
                    driveletter = chr(ord(driveletter) + 1)

                disk_conf = disk_conf + disk_string
                disk_dict = {disk_type:abspath}
                VM_Disks.append(disk_dict)

        network_conf = ""
        i = 3
        netcount = 0

        machine_data_macs = []
        for machinemac in machinemacs:
            for name, mac in machinemac.items():
                if name == machine_name:
                    machine_data_macs.append(mac)

        for network in details.get("Network", []):
            vm_mac = machine_data_macs[netcount]
            nic_model = network[0]
            network_name = network[1]
            network_string = f"""<interface type='network'>
                    <mac address='{vm_mac}'/>
                    <source network='{network_name}_{session_id}'/>
                    <model type='{nic_model}'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x0{i}' function='0x0'/>
                </interface>
                """
            network_conf = network_conf + network_string
            i = i+2
            netcount = netcount + 1

        machine_data_ips = []
        for machineip in machineips:
            for name, ip in machineip.items():
                if name == machine_name:
                    machine_data_ips.append(ip)

        machine_name = f"{machine_name}_{session_id}"
        vm_xml = generate_vm_config(machine_name, details.get("Memory"), details.get("CPUCores"), vnc_port, network_conf, disk_conf)
        #print(vm_xml)
        create_persistent_virtual_machine(machine_name, vm_xml)

        machine_data = {
            "Machine_Name": machine_name,
            "CPUCores": details.get("CPUCores"),
            "Memory": details.get("Memory"),
            "Networks": details.get("Network", []),
            "Disks": VM_Disks,
            "VNC_Port": vnc_port,
            "machine_data_ips": machine_data_ips,
            "machine_data_macs": machine_data_macs
            }

        WriteSessionData("machine", machine_data, session_id)

    return vm_vnc_ports

def ConfigureGuac(vm_vnc_ports, session_id):
    guac_admin_auth_token = generate_authToken(GUACAMOLE_ADMIN_UNAME, GUACAMOLE_ADMIN_PASS, GUACAMOLE_API_URL)
    session_user_credentials = create_guacamole_user(guac_admin_auth_token, GUACAMOLE_API_URL)
    sftp = "false"

    guac_connection_names = []
    for vnc_port in vm_vnc_ports:
        for machine, port in vnc_port.items():
            machine_name = machine
            machine_port = port

        conn_name = f"{machine_name}_{session_id}"
        connection_id = create_guacamole_connections(guac_admin_auth_token, conn_name, machine_port, sftp, GUACAMOLE_API_URL)
        session_username = session_user_credentials["username"]
        set_user_permissions(session_username, connection_id, guac_admin_auth_token, GUACAMOLE_API_URL)
        guac_connection_names.append({f"{conn_name}": f"{connection_id}"})

    session_user_auth_token = generate_authToken(session_user_credentials["username"], session_user_credentials["password"], GUACAMOLE_API_URL)
    session_client_urls = get_client_url(session_user_auth_token, f"{GUAC_SECURITY}://{GUACAMOLE_URL}")

    guac_data = {
        "Connection_Name": conn_name,
        "Session_User": session_user_credentials["username"],
        "Session_Password": session_user_credentials["password"],
        "Session_Auth_Token": session_user_auth_token,
        "Session_Connection_Names": guac_connection_names,
        "Session_Client_URLs": session_client_urls
        }

    WriteSessionData("guacamole", guac_data, session_id)

    return guac_data



def PauseSession(session_id):
    guac_admin_auth_token = generate_authToken(GUACAMOLE_ADMIN_UNAME, GUACAMOLE_ADMIN_PASS, GUACAMOLE_API_URL)
    session_dir = os.path.join(f"sessions", f"{session_id}")
    session_file = os.path.join(f"sessions/{session_id}", "session.json")
    try:
        with open(session_file, 'r') as file:
            session = json.load(file)
    except FileNotFoundError:
        print(session_file)
        print(f"Session {session_id} not found. Are you sure that is correct?")
        return None

    machines = session[session_id]["VMinfo"]
    machine_names = list(machines.keys())
    for machine_name in machine_names:
        power_off_vm(machine_name)

    networks = session[session_id]["Networkinfo"]
    network_names = list(networks.keys())
    for network_name in network_names:
        pause_internal_network(network_name)

    guac_connections = session[session_id]["Guacamole"]["Session_Connection_Names"]
    session_user = session[session_id]["Guacamole"]["Session_User"]
    for guac_connection in guac_connections:
        for connection_name, connection_id in guac_connection.items():
            revoke_user_permissions(session_user, connection_id, guac_admin_auth_token, GUACAMOLE_API_URL)

    os.remove(f"./sessions/{session_id}/lab_page.html")
    print(f"Session {session_id} has been paused sucessfully!")

    return None

def ResumeSession(session_id):
    guac_admin_auth_token = generate_authToken(GUACAMOLE_ADMIN_UNAME, GUACAMOLE_ADMIN_PASS, GUACAMOLE_API_URL)
    session_dir = os.path.join(f"sessions", f"{session_id}")
    session_file = os.path.join(f"sessions/{session_id}", "session.json")

    try:
        with open(session_file, 'r') as file:
            session = json.load(file)
    except FileNotFoundError:
        print(f"Session {session_id} not found. Are you sure that is correct?")
        return None

    culab = session[session_id]["Metadata"]["CourseLab"].split('/')
    coursename = culab[0]
    labname = culab[1]
    course_dir = f"courses/{coursename}"
    lab_to_run = f"{course_dir}/labs/{labname}.json"

    with open(lab_to_run, 'r') as file:
        lab = json.load(file)

    instructions = lab["TestLab"]["Instructions"]
    file.close()

    networks = session[session_id]["Networkinfo"]
    network_names = list(networks.keys())
    for network_name in network_names:
        resume_internal_network(network_name)

    machines = session[session_id]["VMinfo"]
    machine_names = list(machines.keys())
    for machine_name in machine_names:
        power_on_vm(machine_name)

    guac_connections = session[session_id]["Guacamole"]["Session_Connection_Names"]
    session_user = session[session_id]["Guacamole"]["Session_User"]
    for guac_connection in guac_connections:
        for connection_name, connection_id in guac_connection.items():
            set_user_permissions(session_user, connection_id, guac_admin_auth_token, GUACAMOLE_API_URL)

    session_user_auth_token = generate_authToken(session[session_id]["Guacamole"]["Session_User"], session[session_id]["Guacamole"]["Session_Password"], GUACAMOLE_API_URL)
    Session_Client_URLs = session[session_id]["Guacamole"]["Session_Client_URLs"]
    guac_data = {
        "Session_Auth_Token": session_user_auth_token,
        "Session_Client_URLs": Session_Client_URLs
    }

    GenerateLab(GUAC_FULL_URL, guac_data, session_id, instructions, 1)

    print(f"Session {session_id} has been resumed sucessfully!")

    return None

def DestorySession(session_id):
    guac_admin_auth_token = generate_authToken(GUACAMOLE_ADMIN_UNAME, GUACAMOLE_ADMIN_PASS, GUACAMOLE_API_URL)
    session_dir = os.path.join(f"sessions", f"{session_id}")
    session_file = os.path.join(f"sessions/{session_id}", "session.json")
    try:
        with open(session_file, 'r') as file:
            session = json.load(file)
    except FileNotFoundError:
        print(f"Session {session_id} not found. Are you sure that is correct?")
        return None

    machines = session[session_id]["VMinfo"]
    machine_names = list(machines.keys())
    for machine_name in machine_names:
        power_off_vm(machine_name)
        delete_virtual_machine(machine_name)


    networks = session[session_id]["Networkinfo"]
    network_names = list(networks.keys())
    for network_name in network_names:
        delete_internal_network(network_name)

    guac_connections = session[session_id]["Guacamole"]["Session_Connection_Names"]
    guac_user = session[session_id]["Guacamole"]["Session_User"]
    for guac_connection in guac_connections:
        for connection_name, connection_id in guac_connection.items():
            delete_guacamole_connections(guac_admin_auth_token, connection_id, GUACAMOLE_API_URL)
    delete_guacamole_user(guac_admin_auth_token, guac_user, GUACAMOLE_API_URL)

    shutil.rmtree(session_dir)

    print(f"Session {session_id} has been destroyed sucessfully!")

    return None

def startLab(labnames):
    culab = labnames.split('/')
    course = culab[0]
    labname = culab[1]
    course_dir = f"courses/{course}"
    lab_to_run = f"{course_dir}/labs/{labname}.json"

    with open(lab_to_run, 'r') as file:
        lab = json.load(file)

    machines = lab["TestLab"]["Machines"]
    networks = lab["TestLab"]["Networks"]
    instructions = lab["TestLab"]["Instructions"]

    session_id, vm_vnc_ports = CreateSession(machines, course, labname)
    guac_data = ConfigureGuac(vm_vnc_ports, session_id)
    GenerateLab(GUAC_FULL_URL, guac_data, session_id, instructions, 0)
    CreateVM(machines, networks, vm_vnc_ports, session_id, course_dir)
    file.close()

    return session_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CyberLab Demo Program")
    parser.add_argument("--newsession", action="store", help="Starts a new session")
    parser.add_argument("--destorysession", action="store", help="--destorysession [session-id] will stop and delete the VMs, Guacamole connections/users and files for the session")
    parser.add_argument("--pausesession", action="store", help="--pausesession [session-id] will stop VMs and revoke guacamole permissions until session is resumed")
    parser.add_argument("--resumesession", action="store", help="--resumesession [session-id] will resume VMs and add guacamole permissions to the session user")
    args = parser.parse_args()

    if args.newsession:
        print("Building your session. Please wait")
        print("Errors regarding iso file permission from QEMU/Libvirt can be ignored")
        print("")
        session_id = startLab(args.newsession)
        print("")
        print(f"Session {session_id} is now ready. You can access VMs directly by opening ./sessions/{session_id}/lab_page.html")
        print("")
        print(f"TO DESTORY THIS SESSION, run 'python3 cyberlab_concept.py --destorysession {session_id}' NOTE: This will stop and delete the VMs, Guacamole connections/users and files for this session")
    elif args.destorysession:
        print(f"Destorying Session {args.destorysession}")
        DestorySession(args.destorysession)
    elif args.pausesession:
        print(f"Pausing Session {args.pausesession}")
        PauseSession(args.pausesession)
    elif args.resumesession:
        print(f"Resuming Session {args.resumesession}")
        ResumeSession(args.resumesession)
    else:
        print("Invaild Option")

