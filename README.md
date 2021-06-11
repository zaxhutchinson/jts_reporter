# JTS Reporter

## Description
The goal of this project is to provide a way to visualize the current and historical state of ongoing (or completed) [JTS games](https://www.johntillersoftware.com).

I have a tendency to play the monster scenarios, which involve many, many units over many, many turns. These require planning and an understanding of one's forces above the scale of individual units. It can be difficult to grasp the state of one's forces above the unit level, if, for example, a formation is comprised of 30-40 units. The game engine does not provide much in the way of visualization beyond the map on which the game is played.

## Current State
Early development. The current version will load up save games and oob files, reading in all unit data. Currently, it can display on-map strength and fatigue of units, by formation, for the current turn.

## How to use
The project uses Python3 and tkinter. Therefore, currently, all you need is a copy of Python3. If you are on Windows, make sure you check the box during installation to add Python3 to the path (environment variables).

JTS Reporter requires access to the .oob file used by the scenario and any game files you want to evaluate. These should be in the same directory. An easy way to do this is just copy the .oob file into your save game directory.

While the JTS Reporter does store game turn data, it reads game .btl files lexicographically by their file name. If you want to analyze multiple files chronologically, you will need to name them in the order they occurred. The JTS Reporter assumes lexicographic order equals chronologic order. NOTE: You can have more than one save for a given turn. Example:

    - 000_n44.btl
    - 001_n44.btl
    - etc.

To can invoke the reporter by typing into the terminal/shell:

*python main.py dir=path/to/game/files*

For example:

*python main.py dir=saves/N44_Allies*

Of course, if you're on Linux/mac, you will need to type *python3* instead of *python*. NOTE: On Windows, sometimes Python must be invoke by using just *py* instead of *python*. Never bothered to look up why.

JTS Reporter will read all .btl files in this directory and look for an .oob file there, too. You can use absolute or relative paths.

## Goals
Eventually, I hope to include the ability to generate graphs and location specific reports.
