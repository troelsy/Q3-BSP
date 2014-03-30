Q3-BSP
======
What is this?
-----
This is a module for Python used to load Quake 3 Arena BSP files into readable data.


TL;DR - Too Long; Didn't Read
------
Download **LoadBSP.py** and **surfaceflags.py**  
All colors are in RGBA and use the get() method to retrive data from the BSP file.  
  
Example of use:  
```
import LoadBSP
bsp = LoadBSP.BSP('maps/q3tourney6.bsp')

for texture in bsp.get("textures"):
    print texture[0]
```
  
These are the possible commands for get:  
```
"entities", "textures", "planes", "nodes", "leafs", "leaffaces", "leafbrushes", "models", "brushes"
"brushsides", "vertices", "meshverts", "effects", "faces", "lightmaps", "lightvols", "visdata"
```
(These names refer to the names of the lumps given here:
["Unofficial Quake 3 Map Specs"](http://www.mralligator.com/q3/))

Detailed explanation
------

#### Requirements
This module has been tested on Python 2.6.5. It will probably work on 2.7.x too, but it hasn't been
tested.  
You will need "LoadBSP.py" for a minimal setup. If you want to read/translate texture flags, you'll
have to download "surfaceflags.py" too. surfaceflags.py is a translation of
[surfaceflags.h](https://github.com/id-Software/Quake-III-Arena/blob/master/code/game/surfaceflags.h)
provided by ID software's GitHub.
I assume that you have read the article,
["Unofficial Quake 3 Map Specs"](http://www.mralligator.com/q3/), before using this module.

#### How to use
This is a module for Python used to load BSP maps into readable data. The interface of the module is
really simple; when creating an instance of the LoadBSP class, you tell what BSP file to load using
the "fname" argument and the map will then begin loading. When the map is loaded, you can
use the get() method to retrive the data of each "lump". Here is an example, on how to print all the
texture paths:  

```
import LoadBSP
bsp = LoadBSP.BSP('maps/q3tourney6.bsp')

for texture in bsp.get("textures"):
    print texture[0]
```
  
Please, read the documention on how to use the get() method.  

#### Compatability
The lightmap is generated from bitmaps into images using PyGame. If you don't like PyGame, you can
easily change the function to use another module. Just search for "_readLightmap" and change the
PyGame references to you prefered   
  
Besides PyGame, this modules depends on GameObjects 0.3 (Links to all the modules can be found at
the bottom of this document). The GameObjects is just for 3D vectors, and as with lightmapping, this
can easily be changed. If you want to use, let's say, numpy, you'll have to remove the line that
imports gameobjects ("from gameobjects.vector3 import *") and write "import numpy" instead. After
that, locate the method, _convertEntityType, and replace "Vector3" with "numpy.array" - that's it!  
  
  
Thanks to
======
Thanks to "ThomasEgi" from [panda3d.org](https://panda3d.org). This module is based on the code, he
provided in this thread:
[panda3d.org...t=7920](https://www.panda3d.org/forums/viewtopic.php?t=7920)  
Thanks to "Kekoa Proudfoot" for the ["Unofficial Quake 3 Map Specs"](http://www.mralligator.com/q3/)

Links
======
####Sources
["Unofficial Quake 3 Map Specs"](http://www.mralligator.com/q3/)  
[panda3d.org](https://panda3d.org)  

####Non-standard modules
[gameobjects](https://pypi.python.org/pypi/gameobjects)  
[pygame 1.9.1](http://www.pygame.org/download.shtml)  
