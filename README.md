# CyberLab-Concept
Proof of concept command line version of CyberLab Simulator


# Depracation Notice:
**This version will no longer be maintained. CyberLab Simuator will now be 100% flask based If you want a simple, single-user/development version of CyberLab Simulator please refer to the Daemon Repositiory https://github.com/andrewfer000/CyberLab-Daemon**

## What is it
CyberLab automates the management of Apache Guacamole and Libvirt QEMU Virtual Machines & Networks for use in temporary lab environments. Labs are defined in JSON files in their respective courses. Lab environments are very customisable. When you run a lab it creates a new "session". A session is made of a JSON file which tracks what resources (VMs, Networks, Guacamole User/Connections) is owned by that session. Sessions can be paused, resumed, and destoryed. A Lab interface HTML file is provided in each session's directory in ./session/session_id. 

This version of the software is for testing & development purposes specifically in regards to the backend (The part the manages QEMU, Guacamole, and the Sessions for a given back-end host). THIS IS NOT A COMPLETE SOLUTION FOR USE IN SCHOOLS OR TRAINING LABS! One day, this part will be known as the "Daemon"/"Backend" in a real deployment. 

## The Finished Product 
This is not available yet since I need to build a whole frontend and backend API service. Do not expect this for some time. The main goal is to get this version up and running. 

## Benifits
**NOTE:** This benifits section applies to the FINISHED PRODUCT which does not exist yet

### For Trade Schools and Universities
1. Free and Open Source Software. Use and modify to your hearts content.
2. Deploy on your own systems. Keep your data safe.
3. Instructors and Administrators have full control.
4. Low cost to operate. All involved software is Free and Open Source. (Linux, (Apache/Nginx), Python, MySQL, Apache Guacamole, Libvirt/QEMU/KVM)
5. Web based access. No special software or user configurations required. Works with Firefox and Chromium based browsers. (Will likley work with any browser that can support HTML5, iframes, and HTMX)
6. LMS intergration (Far goal).
7. Scales to your needs. Deploy the backend (QEMU/KVM, MySQL, Apache Guacamole) on as many servers as you need. 
8. Secure and isolated. VMs and Networks are randomiszed and destoryed if inactive or lab is complete
9. Lab Session tracking is saved allowing for auditing. 
10. Paid Support, SLAs, and Whitelabeling Services will become available

### For Instructors and Lab Desginers
1. Design and Build Labs using your own VM images and use JSON code to design your lab. It's YOUR VMs, YOUR curriculum, YOUR labs. 
2. Reproducable Lab Environments. Same lab and results with every run.
3. Add Questions and "Checkers" to your labs for automatic grading. 
4. No setup for students. Once your course and labs are deployed. Enrolled students just click and run.
5. Courses based on popular curriculums will be made available for purchace in the future. Buy, Deploy, Run.
6. See student's progress. 

### For Students
1. Login, Click lab, and Learn! No setup required.
2. No powerful system required. Complete your labs on a chromebook!
3. Complete your labs from anywhere, any time! No need to spend time in a physical lab! 
4. No longer need to buy costly access to online lab simulators to complete your work. (Unless your university charges)
5. Mess up? Just reset and try again. Exam prep? Re-run labs to drill in those concepts! 

## Completion

### What is complete
1. Automatic Guacamole Management
2. Automatic QEMU and Network Management
3. Session creation and tracking
4. Session Lab Interface generation
5. Session pausing
6. Session resume
7. Session destory
8. Generate Lab Interface with instrustions and questions (Features still being added)

### What is incomplete
1. Lab JSON checking and validaton (Be careful when writing your own)
2. Lab Checkers
3. Remote user testing (Localhost use only right now)

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
Labs are part of courses. Courses contain vm_images directory (virtual hard drives and isos used for your labs) and a labs directory. If you download the testcourse and unzip it into the courses directory and run the new session command the lab should run without issues. As long as testcourse and it's files (testcourse/vm_images/myvm.qcow2, testcourse/vm_images/test.iso, testcourse/labs/testlab.json) are in-tact you can run the lab.

### Creating your first session
Learn the options with `python3 cyberlab_concept.py --help`
Create a new session based on the testlab with `python3 cyberlab_concept.py --newsession testcourse/testlab`
*Record The session ID for use with other commands! For example, uU47md3QQG will be used to represent sessions in upcomming commands. Be sure to use YOUR session id*


1. Pause your session with `python3 cyberlab_concept.py --pausesession uU47md3QQG`
2. Resume your session with `python3 cyberlab_concept.py -resumesession uU47md3QQG`
3. Destory your session with `python3 cyberlab_concept.py --destorysession uU47md3QQG`

Access the VMs by opening the HTML file in your session directory

## Goals

### Main Goals
- Generate a reproducable lab using JSON code
- Auto-generate web UI for lab
- Create documentation on how to use this concept software

### Possible Goals
- Basic Flask API to control VM power state from the web UI
- Basic Flask API to test checkers and question submissions
- Time limits and background daemon to auto-destory abandoned labs

### Won't implement
- MacOS VM support (Legal reasons)
- Full multi-user system (this is for the main software)


## Screenshots

#### Creating a session from the lab
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/7c2b3fc9-ea33-4779-99d5-25c05dc609b4)

#### Directories and Files in the session's folder
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/353b2f65-18d6-4871-85f0-4695053064ce)

#### Lab Interface
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/82f633e6-a909-47e3-86cd-848fdae7725a)

#### Session File Snipit
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/a2afb779-db58-4262-a2b0-bdf171891255)

#### Destory the session
![image](https://github.com/andrewfer000/CyberLab-Concept/assets/9620913/2dec8b5f-995c-474a-b507-ddf138914a00)

