# JTS Reporter

## Description
The goal of this project is to provide a way to visualize the current and historical state of ongoing (or completed) [JTS games](https://www.johntillersoftware.com). Currently, the reporter supports the Panzer Campaigns series. Depending on the format of save files, it might work with other titles, too.

I have a tendency to play the monster scenarios, which involve many, many units over many, many turns. These require planning and an understanding of one's forces above the scale of individual units. It can be difficult to grasp the state of one's forces above the unit level, if, for example, a formation is comprised of 30-40 units. The game engine does not provide much in the way of visualization beyond the map on which the game is played.

## Current State
Early development.

## How to use

**Dependencies**
- Python 3
    - Download latest and install from python.org.
    - Make sure you check the box 'Add to PATH' on the install splash. It's usually at the very bottom.
- Plotly
    - Once Python 3 is installed, to install the plotly plotting library, open your powershell (windows), terminal (mac/linux) and type: 
        *pip install plotly*
    - This will install the plotly using pip.

**Installing**
- There is nothing to install. Just clone or download the JTS Reporter repository.
- Make sure the *config.ini* file is correct for your setup.
    - **side**: should be set to the side you want to see [allies or axis]. Default set to *allies*. For Panzer Campaigns all nations fall into one or the other category.
    - **save_dir**: should be set to the path containing your save files AND the .oob file. By default it looks for the saves/oob in the same directory (i.e. it assumes the jtsreporter source is in your save dir).

**Running**
- Again, open your powershell (windows) or terminal, navigate to the directory containing the JTS Reporter source and run:

*python start.py*

Of course, if you're on Linux/mac, you will need to type *python3* instead of *python*. NOTE: I have not tested v0.04 on linux/mac.


## Plots and Graphs
IMPORTANT: JTS Reporter as of version 0.04 no longer displays the plots in the application itself.

Currently, JTS Reporter uses Plotly to show plots and graphs. To display the graphs, Plotly uses a default renderer which might vary by machine. For example, on my Windows 10 partition it uses Microsoft Edge to display the plots. This might differ on your machine.

## OOB and Save Files
JTS Reporter requires access to the .oob file used by the scenario and any game files you want to evaluate (currently only .btl files). These need to be in the same directory. An easy way to do this is just copy the .oob file into your directory where you are storing saves (and unzip jtsreporter into the save dir). If you're not sure which .oob file the scenario is using, you can open the scenario file in a text editor and look at line 14. Or you can probably find it in the scenario editor program included with JTS games.

### Multiple save files
JTS Reporter is designed to read in multiple save game files. While the JTS Reporter does store game turn data, it reads game .btl files and stores their data lexicographically by the file name. If you want to analyze multiple files chronologically, you will need to name them in the order they occurred. The JTS Reporter assumes lexicographic order equals chronologic order. NOTE: You can have more than one save for a given turn. Example of file names:

    - 000_n44.btl
    - 001_n44.btl
    - etc.

## Goals
Eventually, I hope to include the ability to generate graphs and location specific reports.
