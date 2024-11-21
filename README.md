
# Kirby's Dream Land - AI - Bot Creation

## Project Overview
For this project, I use artificial intelligence to build a bot that plays through part of the game Kirby's Dream Land. Additionally, I created a system for replaying the movements the AI made throughout its journey. This was be done using a pipeline for the move made and the number of frames the move should be held down for. A description of the files found in this project are shown below:

| File/Folder             | Description                                                                      |
|-------------------------|----------------------------------------------------------------------------------|
| project.py              | The driver of the program                                                        |
| get_data.py             | Program was used to generate the data.json in the KirbysDreamLand-GameBoy Folder |
| KirbysDreamLand-GameBoy | The integrated game KirbysDreamLand                                              |
| data                    | This folder is where all the model data and recordings are stored                |

## Build Instructions

First, ensure python version 8.0 is installed, it can be installed [here](https://www.python.org/downloads/release/python-380/).

Next, go to where python is installed in the terminal/cmd prompt using 

```sh
cd <directory>
```

The location is different based on the operating system. For windows, it is ```C:\Users\<user>\AppData\Local\Programs\Python\Python38```, for linux run the following command to find the path:

```
which python38
```

Once in the directory, on the command prompt, run the following commands (on windows, replace python with python.exe):

```sh
python -m pip install gym-retro
python -m pip install gym==0.21
python -m pip install numpy
python -m pip install scikit-learn
python -m pip install random
python -m pip install time
python -m pip install tkinter
```

Next, in a separate window, move the KirbysDreamLand-GameBoy folder to the following directory: 
```sh
<directory of python installation>/Lib/site-packages/retro/data/stable/
```

Go back to the terminal/cmd window and run the following command, replace directory with the location of the KirbysDreamLand-GameBoy folder (on windows, replace python with python.exe):

```sh
python -m retro.import <directory>
```

Now, you can open idle (python version 8.0) and open->run project.py to execute the project. 

## Project Usage

A video demonstarting the project can be found below:

[![kirby](https://img.youtube.com/vi/bZR1KuypYtM/0.jpg)](https://youtu.be/bZR1KuypYtM)
