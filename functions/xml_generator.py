from jinja2 import Template

def generate_vm_config(vm_name, vm_ram, vm_vcpu, vnc_port, network_conf, disk_conf):
    vm_ram = int(vm_ram) * 1024
    xml_config_preprocess = """
        <domain type='kvm'>
            <name>{{vm_name}}</name>
            <memory unit='KiB'>{{vm_ram}}</memory>
            <vcpu placement='static'>{{vm_vcpu}}</vcpu>
            <os>
                <type arch='x86_64' machine='pc-i440fx-2.12'>hvm</type>
                <boot dev='hd'/>
            </os>
            <features>
                <acpi/>
                <apic/>
                <vmport state="off"/>
            </features>
            <cpu mode="host-passthrough" check="none" migratable="on"/>
            <clock offset="utc">
                <timer name="rtc" tickpolicy="catchup"/>
                <timer name="pit" tickpolicy="delay"/>
                <timer name="hpet" present="no"/>
            </clock>
            <on_poweroff>destroy</on_poweroff>
            <on_reboot>restart</on_reboot>
            <on_crash>destroy</on_crash>
            <pm>
                <suspend-to-mem enabled="no"/>
                <suspend-to-disk enabled="no"/>
            </pm>
            <devices>
                <emulator>/usr/bin/qemu-system-x86_64</emulator>
                {{disk_conf}} {{network_conf}}<input type="tablet" bus="usb">
                <address type="usb" bus="0" port="1"/></input>
                    <video>
                    <model type='qxl' vram='16384' heads='1'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
                </video>
                <graphics type='vnc' port='{{vnc_port}}' autoport='no' listen='0.0.0.0'/>
            </devices>
        </domain>
    """

    template = Template(xml_config_preprocess)
    data = {
    "vm_name": f"{vm_name}",
    "vm_ram": f"{vm_ram}",
    "vm_vcpu": f"{vm_vcpu}",
    "vnc_port": f"{vnc_port}",
    "network_conf": f"{network_conf}",
    "disk_conf": f"{disk_conf}"
    }
    xml_config = template.render(data)
    return xml_config

def generate_net_config(network_name, dh_range_start, dh_range_end, dhcp_leases, bridge_conf):

    network_xml_preprocess = """
    <network>
        <name>{{network_name}}</name>
        {{bridge_conf}}
            <dhcp>
                <range start='{{dh_range_start}}' end='{{dh_range_end}}'/>
                {{dhcp_leases}}
            </dhcp>
        </ip>
    </network>
    """

    data = {
    "network_name": f"{network_name}",
    "bridge_conf": f"{bridge_conf}",
    "dh_range_start": f"{dh_range_start}",
    "dh_range_end": f"{dh_range_end}",
    "dhcp_leases": f"{dhcp_leases}"
    }

    template = Template(network_xml_preprocess)
    network_xml = template.render(data)
    return network_xml

