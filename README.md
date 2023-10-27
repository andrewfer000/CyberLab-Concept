# CyberLab-Concept
Proof of concept command line version of CyberLab

## What is it
CyberLab automates the management of Apache Guacamole and Libvirt QEMU Virtual Machones & Networks for use in temporary lab environments. Labs are defined in JSON files in their respective courses. Lab environments are very customisable. When you run a lab it creates a new "session". A session is made of a JSON file which tracks what resources (VMs, Networks, Guacamole User/Connections) is owned by that session. Sessions can be paused, resumed, and destoryed. A Lab interface HTML file is provided in each session's directory in ./session/session_id.   

### What is complete
1. Automatic Guacamole Management
2. Automatic QEMU and Network Management
3. Session creation and tracking
4. Session Lab Interface generation
5. Session pausing
6. Session resume
7. Session destory

### What is incomplete
1. Lab JSON checking and validaton (Be careful when writing your own)
2. Generate Lab Interface with instrustions and questions
3. Lab Checkers
4. Remote user testing (Localhost use only right now)

## Install

### Software and Configuration You need
1. Apache Guacamole setup with MySQL authentication (No Postgres, LDAP, or file based)
2. QEMU/KVM with Libvirt installed on a modern Linux Host. 
3. Python 3.9+ (with modules, see below)

### Python Modules and other Software
1. You should create a venv for this software
2. Install selenium, BeautifulSoup, libvirt, jinja2, requests, pyvirtualdisplay. You may need more. Just install them if needed.
3. You also need to install "xvfb" on your test server
4. You can attempt to run the HTML files and Guacamole behind a reverse proxy like Apache to make sessions available on the network

### Configuration
Edit the config.json to represent your setup. You should only set your Guacamole Admin credentails for now. MAKE SURE YOU USE A GUACAMOLE USER WITH FULL ACCESS! 

## Downloading the TestCourse
As of now the testcourse is recomended to use instead of starting from scrach. Download and extract the testlab/ folder into the courses directory. Feel free to modify it to your needs. If you copy the lab and create a file (say, testlab2.json) or change the name of the course be sure to change it in the `cyberlab_concept.py` file

TestCourse Download: https://drive.google.com/file/d/1jIKv6ErvM6-PKTilCNFpg7h0KEF6dIJe/view?usp=sharing

**NOTE:** Due to the large file size this zip only gets updated every once and awhile and changes to the lab system does change. Please refer to the References directory and use the example lab for the latest changes. For example, "disk" for disk type has been changed to windisk for Windows and lindisk for Linux for compatability reasons. 

## Running
### Information
Right now, There is a lab hardcoded in cyberlab_concept.py. You can change it but if you just want to test this will work. Labs are part of courses. courses contain vm_images directory (virtual hard drives and isos used for your labs) and a labs directory. In the courses/testcourse/labs directory there is a file called testlab.json. This is what is read when building the lab session. You can add/remove networks and VMs as needed and use your own images as long as you place them in the vm_images directory. Detailed documentation on building labs comming soon. 

As long as testcourse and it's files (testcourse/vm_images/myvm.qcow2, testcourse/vm_images/test.iso, testcourse/labs/testlab.json) are in-tact you can run the lab.

### Creating your first session
Learn the options with `python3 cyberlab_concept.py --help`
Create a new session based on the testlab with `python3 cyberlab_concept.py --newsession`
*Record The session ID for use with other commands! For example, uU47md3QQG will be used to represent sessions in upcomming commands. Be sure to use YOUR session id*


1. Pause your session with `python3 cyberlab_concept.py --pausesession uU47md3QQG`
2. Resume your session with `python3 cyberlab_concept.py -resumesession uU47md3QQG`
3. Destory your session with `python3 cyberlab_concept.py --destorysession uU47md3QQG`

Access the VMs by opening the HTML file in your session directory

## Screenshots

#### Creating a session from the lab
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/7c2b3fc9-ea33-4779-99d5-25c05dc609b4)

#### Directories and Files in the session's folder
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/353b2f65-18d6-4871-85f0-4695053064ce)

#### Lab Interface
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/82f633e6-a909-47e3-86cd-848fdae7725a)

#### Session File
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/f8dbbae6-a7f4-44b6-985a-69c102865798)

#### Destory the session
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/2dec8b5f-995c-474a-b507-ddf138914a00)

