import json

# The purpose of this file is to verify a lab will work.
# Notices are the lowest problem level and often involve things such as checker use or relying on DHCP to allocate IP addresses automaticly
# Warnings are raised for problems that should be reviewed such as hardware over-allocation or issues that will likley prevent the lab from working correctly
# Errors are raised if the lab is missing parts or has configuration problems that will prevent the lab from working at all

LAB_TO_RUN = "labs/testcourse/testlab.json"

try:
    with open(LAB_TO_RUN, 'r') as file:
        lab = json.load(file)
except FileNotFoundError:
    print("File not found. Please check the file path.")
    raise
except json.JSONDecodeError:
    print("Error decoding JSON. The file might be corrupted or not in valid JSON format.")
    raise
except Exception as e:
    print(f"An error occurred: {e}")
    raise


ERROR_FOUND = 0
WARN_FOUND = 0
NOTICE_FOUND = 0

Notices = ""
Errors = ""
Warnings = ""

# INSERT CHECK FUNCTIONS HERE. WIP

if ERROR_FOUND != 0:
    print("Errors Found. Your lab will not run unless these are fixed")
    print(Errors)

if WARN_FOUND != 0:
    print("Warnings Found. You should review these before running your lab")
    print(Warnings)

if NOTICE_FOUND != 0:
    print("Notices found. Please test your lab to ensure functionality")
    print(Notices)

if ERROR_FOUND == 0 and WARN_FOUND == 0:
    print("No Errors or Warnings Found. Your Lab is ready to run!")
