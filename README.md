# WoH-SpriteChecker

![intr](https://github.com/Myonmu/WoH-SpriteChecker/assets/62897460/0cb1ca26-13a1-4fd7-9108-0649121c7e1e)


This is a simple python program that checks every pixel of your sprite and determine if their color is correct.

As you may (should) know, the game has a strict palette and your pixels must be one of the defined colors, otherwise transparency/color mapping will not work correctly.

This program detects any pixel that do not match any of the defined colors and convert them to the closest one. 

**Note that as of current version, it can only check 1-bit character sprites.**

## Palette Definition

Currently, the color palette of character sprites is defined as:

1. pure black ( RGB( 0 , 0, 0 ) or HSV( 0, 0, 0 ) )
2. pure white ( RGB( 255, 255, 255 ) or HSV( 0, 0 , 255 ))
3. color at the bottom-left corner of the sprite (regarded by the game as transparent)

**IMPORTANT NOTE**:  though you may use any color as transparency color, when distinguishing between pure white and transparent color, the program checks by saturation value . This means that your transparency color should be as saturated as possible (at least >127).

## Usage

Depending on your preference, you can download the zip file from standalone and run the program without the need of Python environment, or you can simply grab the source code if you have Python and **imageio** installed. The standalone version is also built on Windows and will only work on Windows. 

### Using Standalone
0. Download he standalone exe file
1. put all your sprites in the folder containing the exe
2. launch SpriteChecker.exe, the program will display information on whether pixels are corrected.
3. corrected sprites are stored in a folder named "corrected" under the folder containing the exe.

### Using Python script (source)

You need to have Python and imageio package installed. 

Grab the **SpriteCheckerLite.py** and run it from the command line as if it was a standalone. (Put sprites at the same level as the script, and run the script, find the result in "corrected" folder) 

