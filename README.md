# Digital Filters Python Controller

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Author: Agustin Bassi
Date: April 2019

README file of Digital Filters Controller project

This project only works on Debian based Linux distros.
Also, it's necessary to get installed python3 to run it.

## Requierments

To install this project is necessary to convert to excecutable files install.sh and autorun.sh

```sh
$ chmod +x install.sh
$ chmod +x autorun.sh
```

Optionally change virtual editing path in "config.ini" file

## Installation

Once install.sh is excecutable file, run in terminal:

```sh
$ ./install.sh
```

If you want to see all steps needed to install the project see the content of install.sh script

```sh
$ cat install.sh
```

## Usage

There are two ways to run

### Method 1: Automatically

Excecute automated script that activate virtual environment and then run the main python script.

```sh
$ ./autorun.sh
```

### Method 2: Manually

To run the project manually, first activate the python3 virtual environments described in config.ini file.

```sh
$ source path_to_venv/bin/activate
```

Once virtual environment is activated run application as a module:

```sh
$ python3 src/__main__.py 
$ python3 src/__main__.py -h # to see program help
$ python3 src/__main__.py -c path_to_config_file # to change path of config.ini file
```

## config.ini file

If for some reason the config.ini file is corrupted, copy the content below in the config.ini file to run application with correct parameters.

```sh
[SYSTEM]
virtual_env_path = ~/venvs/dsp_auto

[GENERAL]
config_welcome_message = DSP Controller!
config_wav_original = wavs/guitars.wav
config_wav_modified = wavs/audio_modified.wav

[COMB]
comb_delay = 8
comb_scale = 1.0

[FLANGER]
flanger_max_delay = 0.003
flanger_scale = 1.0
flanger_rate = 0.5

[WAHWAH]
wahwah_damping = 0.05
wahwah_min_cutoff = 300
wahwah_max_cutoff = 3000
wahwah_frequency = 0.4
```

## Tools

### Requierments

To get requierments of the module it is necessary to install pipreqs package

```sh
$ pip install pipreqs
```

To get the requierments of project run:

```sh
$ pipreqs src/ --force
```

This command will create requierments.txt file in src/ folder that contains modules needed by the project.

### Linting

A pep8 linter was used to make the code compilant with this standard.
The modules installed for this requierments was autopep8 and pycodestyle

```sh
$ pip install --upgrade autopep8
$ pip install pycodestyle
```

The linter was excecuted over each file of src folder. The command used was:

```sh
$ autopep8 --in-place --aggressive --aggressive <file_name.py>
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
