#!/bin/bash

# Import $virtual_env_path variable from config.ini
# and remove whitespaces
source <(grep virtual_env_path config.ini | sed 's/ *= */=/g')

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