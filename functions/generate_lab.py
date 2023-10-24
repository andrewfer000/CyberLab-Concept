import json, random, string, os, argparse, shutil
from jinja2 import Environment, FileSystemLoader, Template

def GenerateLab(GUAC_FULL_URL, guac_data, session_id):
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("labpagetest.html.j2")

    i = 1
    vm_buttons = ""
    iframe_content = ""
    for Session_Client_URL in guac_data.get("Session_Client_URLs"):
        ui_vmbutton = f'''<button class="tab-button" onclick="showTab({i})">VM {i}</button>
        '''
        ui_iframe = f'''
            <div class="tab-content" id="tab{i}">
                <iframe id="guacamole-iframe{i}" class="scaled-iframe" src="{GUAC_FULL_URL}/{Session_Client_URL}?token={guac_data.get("Session_Auth_Token")}" width="1280" #height="720"></iframe>
        </div>
        '''
        i = i + 1
        vm_buttons =  vm_buttons + ui_vmbutton
        iframe_content = iframe_content + ui_iframe

    data = {
        "vm_buttons": vm_buttons,
        "iframe_content": iframe_content
        }

    output = template.render(data)
    output_file_path = f"./sessions/{session_id}/lab_page.html"

    with open(output_file_path, "w") as output_file:
        output_file.write(output)

    return None
