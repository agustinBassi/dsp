#!/bin/bash

# Import $virtual_env_path variable from config.ini
# and remove whitespaces
source <(grep virtual_env_path config.ini | sed 's/ *= */=/g')

echo "VENV path is: $virtual_env_path"

source $virtual_env_path/bin/activate

python3 -m src
