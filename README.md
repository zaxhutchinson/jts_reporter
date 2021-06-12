# JTS Reporter

## Description
The goal of this project is to provide a way to visualize the current and historical state of ongoing (or completed) [JTS games](https://www.johntillersoftware.com). Currently, the reporter supports the Panzer Campaigns series. Depending on the format of save files, it might work with other titles, too.

I have a tendency to play the monster scenarios, which involve many, many units over many, many turns. These require planning and an understanding of one's forces above the scale of individual units. It can be difficult to grasp the state of one's forces above the unit level, if, for example, a formation is comprised of 30-40 units. The game engine does not provide much in the way of visualization beyond the map on which the game is played.

## Current State
Early development.

## How to use
# Dependencies
The project uses Python3 and tkinter. Therefore, currently, all you need is a copy of Python3. If you are on Windows, make sure you check the box during installation to add Python3 to the path (environment variables).

# OOB and Save Files
JTS Reporter requires access to the .oob file used by the scenario and any game files you want to evaluate. These need to be in the same directory. An easy way to do this is just copy the .oob file into your directory where you are storing saves. If you're not sure which .oob file the scenario is using, you can open the scenario file in a text editor and look at line 14. Or you can probably find it in the scenario editor program included with JTS games.

While the JTS Reporter does store game turn data, it reads game .btl files lexicographically by their file name. If you want to analyze multiple files chronologically, you will need to name them in the order they occurred. The JTS Reporter assumes lexicographic order equals chronologic order. NOTE: You can have more than one save for a given turn. Example of file names:

    - 000_n44.btl
    - 001_n44.btl
    - etc.

# ini File - Side to display
Set the value for *side* to the side you wish to display (e.g. allies or axis). JTS Reporter will only display one or the other to keep players from accidentally seeing info from the other side.

# Running JTS Reporter
You can invoke the reporter by typing into the terminal/shell:

*python main.py dir=path/to/save/files*

For example:

*python main.py dir=saves/N44_Allies*

Of course, if you're on Linux/mac, you will need to type *python3* instead of *python*. NOTE: On Windows, sometimes Python must be invoked by using just *py* instead of *python*. Never bothered to look up why.

JTS Reporter will read all .btl files in this directory and look for an .oob file there, too. You can use absolute or relative paths.

## Goals
Eventually, I hope to include the ability to generate graphs and location specific reports.
