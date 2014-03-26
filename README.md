Q3-BSP
======

TL;DR
------
Download **LoadBSP.py** and **surfaceflags.py**  
All colors are in RGB/RGBA and use the get() method to retrive data from the BSP file.  
  
Example:  
```
import LoadBSP
bsp = LoadBSP("maps/q3tourney6.bsp")

for texture in bsp.get("textures"):
    print texture
```
  
These are the possible get commands:  
```
"entities"
"textures"
"planes"
"nodes"
"leafs"
"leaffaces"
"leafbrushes"
"models"
"brushes"
"brushsides"
"vertices"
"meshverts"
"effects"
"faces"
"lightmaps"
"lightvols"
"visdata"
```
(These names refer to the names given here:
["Unofficial Quake 3 Map Specs"](http://www.mralligator.com/q3/))

Detailed explanation
------


Python 2.6.5
surfaceflags.py



This is a module for Python used to load BSP maps into readable data. The interface of the module is
really simple; when creating an instance of the LoadBSP class, you tell what BSP file to load using
the fname argument and the map will then begin loading. When the map is loaded, you can
use the get() method to retrive the data of each "lump". Here is an example:  

```
import LoadBSP
bsp = LoadBSP("maps/q3tourney6.bsp")

for texture in bsp.get("textures"):
    print texture
```
  
Please read the documention on how to use the get() method.  

#### Compatability
The lightmap is generated from bitmaps into images using PyGame. If you don't like PyGame, you can
easily change the function, _readLightmap, to use another module.  
  
Besides PyGame, this modules depends on GameObjects 0.3 (Links to all the modules can be found at
the bottom of this document). The GameObjects is just for 3D vectors, and as with lightmapping, this
can easily be changed. If you want to use, let's say, numpy, you'll have to remove the line that
imports gameobjects ("from gameobjects.vector3 import *") and write "import numpy" instead. After
that, locate the method, _convertEntityType, and replace "Vector3" with "numpy.array" - that's it!  
  
  
  
Links
======
Thanks to
-------
Thanks to "ThomasEgi" from [panda3d.org](https://panda3d.org). This module is based on the code, he
provided in this thread: [panda3d.org...t=7920](https://www.panda3d.org/forums/viewtopic.php?t=7920)
Thanks to "Kekoa Proudfoot" for the ["Unofficial Quake 3 Map Specs"](http://www.mralligator.com/q3/)

Modules
------
[gameobjects](https://pypi.python.org/pypi/gameobjects)  
[pygame 1.9.1](http://www.pygame.org/download.shtml)  
