# DSP Python Controller

Author: Agustin Bassi
Date: 04 April 2019

README file of DSP Controller project

This project only works on Debian based Linux distros.
Also, it's necessary to get installed python3

## Requierments

To install this project is necessary to convert to excecutable files install.sh and run.sh

$ chmod +x install.sh
$ chmod +x run.sh

Optionally change virtual editing path in "config.ini" file

## Installation

After make install.sh excecutable run in terminal:

$ ./install.sh

If you want to see all steps needed to install the project see the content of install.sh script

$ cat install.sh

## Usage

There are two ways to run

### Method 1: Automatically

Excecute automated script that activate virtual environment and then run the main python script.

$ ./run.sh

### Method 2: Manually

To run the project manually, first activate the python3 virtual environments described in config.ini file.

$ source path_to_venv/bin/activate

Once virtual environment is activated run application as a module:

$ python3 -m src 

If you want to see help to execute it with different arguments run:

$ python3 -m src -h

## Tools

### Requierments

To get requierments of the module it is necessary to install pipreqs package

$ pip install pipreqs

To get the requierments of project run:

$ pipreqs src/ --force

This command will create requierments.txt file that contains modules needed by the project.

### Linting

A pep8 linter was used to make the code compilant with this standard.
The modules installed for this requierments was autopep8 and pycodestyle

$ pip install --upgrade autopep8
$ pip install pycodestyle

The linter was excecuted over each file of src folder. The command used was:

$ autopep8 --in-place --aggressive --aggressive <file_name.py>


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)