import json, random, string, os, argparse, shutil
from jinja2 import Environment, FileSystemLoader, Template

def GenerateInstructions(instructions):
    number_of_pages = len(instructions)
    i = 1
    lab_content = ""
    while i <= number_of_pages:
        page_header = instructions[f'Page{i}']['Header']
        page_data = instructions[f'Page{i}']['Data']

        page_html = ""

        for item in page_data:
            element = ""

            if "HTMLText" in item:
                text = item["HTMLText"]
                element = f"<p>{text}</p>"
                page_html = page_html + element

            elif "HTMLUList" in item:
                listdata = ""
                listitems = item["HTMLUList"]

                for listitem in listitems:
                    listdata = listdata + f"<li>{listitem}</li>"

                element = f"""
                <ul>
                {listdata}
                </ul>
                """
                page_html = page_html + element

            elif "Question/MultipleChoice" in item:
                question = item["Question/MultipleChoice"][0].split(":")[0]
                options = item["Question/MultipleChoice"][1:]
                answer = item["Question/MultipleChoice"][0].split(":")[1]
                position = 1
                choices = ""
                for option in options:
                    choice = f"""
                    <label>
                        <input type="radio" name="answer" value="{position}"> {option}
                    </label><br>
                    """
                    choices = choices + choice

                question_text = f"<p><b>{question}</b></p>"

                element = f"""
                <form>
                {question_text}
                {choices}
                </form>
                <br>
                """
                page_html = page_html + element

        page_content = f"""
            <div class="sidebar-page" id="page{i}">
                <h2>{page_header}</h2>
                {page_html}
            </div>
            """

        lab_content = lab_content + page_content
        i = i+1

    return lab_content



def GenerateLab(GUAC_FULL_URL, guac_data, session_id, instructions):

    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("labpagetest.html.j2")

    i = 1
    vm_buttons = ""
    iframe_content = ""
    lab_content = GenerateInstructions(instructions)

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
        "iframe_content": iframe_content,
        "lab_content": lab_content
        }

    output = template.render(data)
    output_file_path = f"./sessions/{session_id}/lab_page.html"

    with open(output_file_path, "w") as output_file:
        output_file.write(output)

    return None

