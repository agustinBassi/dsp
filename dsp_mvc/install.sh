#!/bin/bash

source CONFIG.ini

echo "Installing DSP Controller dependences"

sudo apt-get update
sudo apt-get install -y python3-tk
sudo apt-get install -y python3-pip

echo "Creating virtual environment"

python3 -m venv $virtual_env_path

echo "Activating virtual environment"

source $virtual_env_path/bin/activate

echo "Install python deps on venv"

pip install -r src/requirements.txt

echo "Install process exit OK"

# import os
# import sys
# import configparser


# CONFIG_FILE = "CONFIG.ini"
# REQUIERMENTS_FILE = "src/requirements.txt"

# print("Installing DSP Controller dependences")

# try:
#     print("\nUpdating aptitude...\n")
#     pass
#     #os.system("sudo apt-get update")
# except:
#     print("Error while updating apt")
#     sys.exit()

# try:
#     print("\nInstalling tkinter....\n")
#     os.system("sudo apt-get install -y python3-tk")
# except:
#     print("Error while installing tkinter")
#     sys.exit()

# try:
#     print("\nInstalling pip...\n")
#     os.system("sudo apt-get install -y python3-pip")
# except:
#     print("Error while installing python pip")
#     sys.exit()

# try:
#     print("\nReading config file....\n")
#     config = configparser.ConfigParser()
#     config.read(CONFIG_FILE)
#     virtual_env_path = config['VENV']['virtual_env_path']
# except:
#     print("Error while reading config file. Check next things:")
#     print("\t- If there is a file called CONFIG.ini in this folder")
#     print("\t- If the content of file is")
#     print("\n[VENV]")
#     print('virtual_env_path = "/home/juan.bassi/vens/dsp_auto"')
#     sys.exit()

# try:
#     print("\nCreating virtual envirnoment...\n")
#     os.system("python3 -m venv %s" % virtual_env_path)
# except:
#     print("Error while creating virtual environment")
#     sys.exit()

# try:
#     print("\nActivating virtual envionment...\n")
#     os.system("source %s/bin/activate" % virtual_env_path)
# except:
#     print("Error while creating virtual environment")
#     sys.exit()

# try:
#     print("\nInstalling requierments for venv...\n")
#     os.system("pip install -r %s" % REQUIERMENTS_FILE)
# except:
#     print("Error while installing python dependences")
#     sys.exit()

# print("Everything was saccesfully installe. Now excecute ./run.sh to run DSP Controller")


