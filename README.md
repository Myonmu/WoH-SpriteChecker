# WoH-SpriteChecker

![intr](https://github.com/Myonmu/WoH-SpriteChecker/assets/62897460/0cb1ca26-13a1-4fd7-9108-0649121c7e1e)


This is a simple python program that checks every pixel of your sprite and determine if their color is correct.

As you may (should) know, the game has a strict palette and your pixels must be one of the defined colors, otherwise transparency/color mapping will not work correctly.

This program detects any pixel that do not match any of the defined colors and convert them to the closest one. 

## Palette Definition

Currently, the color palette of most sprites (sprites excluding character and enemy) is defined as:

1. pure black ( RGB( 0 , 0, 0 ) or HSV( 0, 0, 0 ) )
2. pure white ( RGB( 255, 255, 255 ) or HSV( 0, 0 , 100 ))
3. light purple ( RGB( 255, 64, 255 ) or HSV(300, 74, 100))
4. dark purple ( RGB( 192, 0, 192 ) or HSV(300, 100, 75))


and for character sprites, there is one extra color:

1. color at the bottom-left corner of the sprite (regarded by the game as transparent)

the equivalent for enemy sprites is simply transparent (alpha = 0)

*Though I write "purple", it is actually closer to magenta, but I was surrounded by magenta-phobic folks thus I deploy the term "purple" instead.*

**IMPORTANT NOTE**:  though you may use any color as transparency color, when distinguishing between pure white and transparent color, the program checks by saturation and value . This means that your transparency color should be as saturated as possible and as bright as possible (upper-right corner of your color picker).
**ANOTHER IMPORTANT NOTE**: since purple (magenta, ahem) is reserved, your transparency color should go nowhere near purple. The program will correct any color that is within 300+-20 hue to the corresponding purple color, so keep this in mind.

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

## How does it segment the colors

### Determine which type of sprite it is  

First, the program checks whether transparency color should be considered (whether it is a character sprite). This is done by checking the size of the sprite against the defined sizes of character sprites (excluding the 18x18 icon sprite).

However, since portrait sprite has the same size as regular event sprites, the program is unable to tell them apart by the simple size rules. To distinguish these two types of sprites, the program detects if the file name contains "**evt**" or "**event**" (case insensitive).

If it is indeed a character sprite, then the bottom left corner of the image is sampled.

### Iterate through the pixels

It is better to visualise it in a color picker:

