import libvirt

LIBVIRTURL = 'qemu:///system'

#-----------------------------------------------------------------------------------------------------
def list_virtual_machines():
    conn = libvirt.open(f"{LIBVIRTURL}")  # Connect to the local QEMU/KVM hypervisor
    if conn is None:
        print(f'Failed to open connection to {LIBVIRTURL}')
        return

    try:
        domain_ids = conn.listDomainsID()
        active_domains = [conn.lookupByID(domain_id) for domain_id in domain_ids]

        inactive_domains = conn.listDefinedDomains()

        print("Active Virtual Machines:")
        for domain in active_domains:
            print(f"ID: {domain.ID()} Name: {domain.name()}")

        print("\nInactive Virtual Machines:")
        for domain_name in inactive_domains:
            print(f"Name: {domain_name}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()

def create_persistent_virtual_machine(vm_name, xml_config):
    try:
        conn = libvirt.open(f"{LIBVIRTURL}")
        if conn is None:
            print(f'Failed to open connection to {LIBVIRTURL}')
            return

        domain = conn.defineXML(xml_config)
        if domain is None:
            print('Failed to define the virtual machine')
            return

        domain.create()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn is not None:
            conn.close()


def power_on_vm(vm_name):
    try:
        conn = libvirt.open(f"{LIBVIRTURL}")
        if conn is None:
            print(f'Failed to open connection to {LIBVIRTURL}')
            return False

        domain = conn.lookupByName(vm_name)
        if domain is None:
            print(f'Virtual machine {vm_name} not found')
            return False

        domain.create()
        return True

    except Exception as e:
        print(f'Error: {e}')
        return False

    finally:
        if conn is not None:
            conn.close()

def power_off_vm(vm_name):
    try:
        conn = libvirt.open(f"{LIBVIRTURL}")
        if conn is None:
            print(f'Failed to open connection to {LIBVIRTURL}')
            return False

        domain = conn.lookupByName(vm_name)
        if domain is None:
            print(f'Virtual machine {vm_name} not found')
            return False

        domain.shutdown()
        return True

    except Exception as e:
        print(f'Error: {e}')
        return False

    finally:
        if conn is not None:
            conn.close()

def delete_virtual_machine(vm_name):
    try:
        conn = libvirt.open(f"{LIBVIRTURL}")
        if conn is None:
            print(f'Failed to open connection to {LIBVIRTURL}')
            return

        domain = conn.lookupByName(vm_name)
        if domain is None:
            print(f"Virtual machine '{vm_name}' not found.")
            return

        domain.undefine()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn is not None:
            conn.close()

def create_transient_virtual_machine(vm_name, vm_xml):
    try:
        conn = libvirt.open(f"{LIBVIRTURL}")
        if conn is None:
            print(f'Failed to open connection to {LIBVIRTURL}')
            return

        conn.createXML(xml_config, 0)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn is not None:
            conn.close()

def create_internal_network(network_xml):
    conn = libvirt.open(LIBVIRTURL)
    network = conn.networkDefineXML(network_xml)

    if network is not None:
        network.create()
    else:
        print("Failed to define internal network.")

    conn.close()

def delete_internal_network(network_name):
    conn = libvirt.open(LIBVIRTURL)
    network = conn.networkLookupByName(network_name)

    if network is not None:
        if network.isActive():
            network.destroy()
        network.undefine()
    else:
        print(f"Network '{network_name}' not found.")

    conn.close()

def pause_internal_network(network_name):
    conn = libvirt.open(LIBVIRTURL)
    network = conn.networkLookupByName(network_name)

    if network is not None:
        if network.isActive():
            network.destroy()
    else:
        print(f"Network '{network_name}' not found.")

    conn.close()

def resume_internal_network(network_name):
    conn = libvirt.open(LIBVIRTURL)
    network = conn.networkLookupByName(network_name)
    if network is not None:
        network.create()
    else:
        print("Failed to define internal network.")

    conn.close()
