
__author__     = "Troels Ynddal"
__copyright__  = "Copyright 2014, Troels Ynddal"
__credits__    = ["Troels Ynddal", "Kekoa Proudfoot", "Thomas Egi"]
__license__    = "GPL v2"
__version__    = "1.0.0"
__maintainer__ = "Troels Ynddal"
__email__      = "troelsynddal.public@gmail.com"
__status__     = "Development"

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# BSP constants
FLOAT    = 4
INT      = 4
UBYTE    = 1
STRING   = 64
LIGHTMAP = 128

# Render module arguments
PYGAME   = 0x10
PIL      = 0x11
NO_GFX   = 0x12 # Python 3D List

# Math module arguments
NUMPY    = 0x1
GAME_OBJ = 0x2
LIST     = 0x3

import struct
import math
#import numpy # https://pypi.python.org/pypi/numpy
#import gameobjects # https://pypi.python.org/pypi/gameobjects

class IllegalFileFormat(Exception): pass
class IllegalMathModule(Exception): pass
class IllegalGFXModule(Exception):  pass

class BSP(object):
    def __init__(self, fname, vector = LIST, gfx = PYGAME, debug = 0):
        self.GFX_module = gfx
        self._setDebugLvl(debug) # Set debugging output level. Default: 0
        self.percentage = 0.0 # Variable for percentage loaded

        # import vector module
        if vector == GAME_OBJ:
            import gameobjects.vector3
            self.Vector = gameobjects.vector3.Vector3
        elif vector == NUMPY:
            import numpy
            self.Vector = numpy.array
        elif vector == LIST:
            self.Vector = self._arrayVector
        else:
            raise IllegalMathModule("Could not recognize math module")

        # Select function for generation of lightmap
        if gfx == PYGAME:
            global pygame
            import pygame
            self._readLightmap = self._readLightmapPyGame
        elif gfx == PIL:
            global Image
            from PIL import Image
            self._readLightmap = self._readLightmapPIL
        elif gfx == NO_GFX:
            self._readLightmap = self._readLightmapNoGFX
        else:
            raise IllegalGFXModule("Could not recognize GFX module")

        self.infile = open(fname,"rb")

        self.lumps = [  ["entities",    self._readEntities,    None],
                        ["textures",    self._readTextures,    None],
                        ["planes",      self._readPlanes,      None],
                        ["nodes",       self._readNodes,       None],
                        ["leafs",       self._readLeafs,       None],
                        ["leaffaces",   self._readLeafsFaces,  None],
                        ["leafbrushes", self._readLeafBrushes, None],
                        ["models",      self._readModels,      None],
                        ["brushes",     self._readBrushes,     None],
                        ["brushsides",  self._readBrushsides,  None],
                        ["vertices",    self._readVertices,    None],
                        ["meshverts",   self._readMeshverts,   None],
                        ["effects",     self._readEffects,     None],
                        ["faces",       self._readFaces,       None],
                        ["lightmaps",   self._readLightmaps,   None],
                        ["lightvols",   self._readLightvols,   None],
                        ["visdata",     self._readVisdata,     None]
                    ]

        self.lumpDict = {} # Generates the lump dictionary for the .get() metode
        for lump in self.lumps:
            self.lumpDict[lump[0]] = []

        # Read header and lumps directory
        self._readHeader()
        self._readLumps()

        # Read data from lumps
        for lump in self.lumps:
            lump[1](*lump[2])
            self.percentage += 1./len(self.lumps)*100

        self.percentage = 100.

    def _arrayVector(self, *args):
        return args

    def get(self, dictName):
        try:
            return self.lumpDict[dictName]
        except KeyError, e:
            raise ValueError("No lump found with that name")
        except:
            raise

    def getPercentage(self, ceil = True):
        if ceil:
            return math.ceil(self.percentage)
        else:
            return self.percentage

    def _setDebugLvl(self, level):
        if level == 0: # No debugging
            self.debug  = False
            self.debug2 = False
            self.debug3 = False
        elif level == 1: # 1. level of detail
            self.debug  = True
            self.debug2 = False
            self.debug3 = False
        elif level == 2: # 2. level of detail
            self.debug  = True
            self.debug2 = True
            self.debug3 = False
        elif level == 3: # 3. level of detail
            self.debug  = True
            self.debug2 = True
            self.debug3 = True
        else:
            raise ValueError("Could not set debugging level to: " + str(level))

    def _readHeader(self):
        if self.debug:
            print
            print "START OF HEADER"

        magic = self.infile.read(INT)
        versionnumber = struct.unpack("<i" , self.infile.read(INT))[0]

        if magic != "IBSP": raise IllegalFileFormat("Target file is not a IBSP file")
        if versionnumber != 0x2e: raise IllegalFileFormat("Expected IBSP version be: 0x2e")

        if self.debug:
            print "magic number:", magic
            print "version number" , hex(versionnumber)
            print "END OF HEADER"
            print

    def _readLumps(self):
        if self.debug: print "START OF LUMPS"

        for lump in self.lumps:
            if self.debug: print lump[0]+" lump", 
            lump[2] = self._readLumpEntry()

        if self.debug: print "END OF LUMPS"
  
    def _readLumpEntry(self):
        lumpEntry = ( struct.unpack("<ii", self.infile.read(INT*2)) )
        if self.debug:
            print lumpEntry

        return lumpEntry

    def _readTexture(self):
        texturename = self.infile.read(STRING).rstrip("\0")
        sourceFlags = struct.unpack("<i", self.infile.read(INT))[0]
        contentFlags= struct.unpack("<i", self.infile.read(INT))[0]

        if self.debug2:
            print
            print "texturename:" , texturename
            print "sourceFlags:",  sourceFlags
            print "contentFlags:", contentFlags

        return (texturename, sourceFlags, contentFlags)

    def _readTextures(self, offset, length):
        if self.debug:
            print
            print "START OF TEXTURES"

        numtextures = length/(STRING+INT+INT) #thats 64chars,4byte int, 4 byte int  
        if self.debug:
            print "Number of Textures", numtextures

        self.infile.seek(offset)
        for i in range(numtextures):
            self.lumpDict["textures"].append(self._readTexture())

        if self.debug2:
            for t in self.lumpDict["textures"]:
                print t

        if self.debug:
            print "END OF TEXTURES"

    def _readLightmapPIL(self):
        texture = Image.new('RGB', (LIGHTMAP,LIGHTMAP), (0,0,0))

        for x in range(LIGHTMAP):
            for y in range(LIGHTMAP):
                texture.putpixel((y, x), struct.unpack("<BBB", self.infile.read(UBYTE*3)) )

        self.lumpDict["lightmaps"].append(texture)

    def _readLightmapPyGame(self):
        texture   = pygame.Surface((LIGHTMAP,LIGHTMAP))
        surfarray = pygame.surfarray.pixels3d(texture)

        for x in range(LIGHTMAP):
            for y in range(LIGHTMAP):
                surfarray[y][x] = struct.unpack("<BBB", self.infile.read(UBYTE*3))

        pygame.surfarray.blit_array(texture, surfarray)
        self.lumpDict["lightmaps"].append(texture)

    def _readLightmapNoGFX(self):
        texture = []

        for x in range(LIGHTMAP):
            texture.append([])
            for y in range(LIGHTMAP):
                texture[x].append(struct.unpack("<BBB", self.infile.read(UBYTE*3)))

        self.lumpDict["lightmaps"].append(texture)

    def _readLightmaps(self, offset, length):
        numLightmaps = length/(LIGHTMAP*LIGHTMAP*3)
        if self.debug:
            print
            print "START OF LIGHTMAPS"
            print "Number of Lightmaps", numLightmaps

        self.infile.seek(offset)
        for i in range(numLightmaps):
            self._readLightmap()

        if self.debug:
            print "END OF LIGHTMAPS"

    def _readMeshverts(self, offset, length):
        self.infile.seek(offset)
        numMeshverts = length/INT

        if self.debug:
            print 
            print "START OF MESHVERTS"
            print "number of meshVertices:", numMeshverts
            print "END OF MESHVERTS"

        for i in range(0,numMeshverts):
            self.lumpDict["meshverts"].append(struct.unpack("<i", self.infile.read(INT))[0])

        if self.debug3:
            for m in self.get("meshverts"):
                print m

    def _readVertex(self):
        vertexPos      = ( struct.unpack(  "<fff", self.infile.read(FLOAT*3)) )
        vertexTexcoord = ( struct.unpack(   "<ff", self.infile.read(FLOAT*2)) )
        vertexLightmap = ( struct.unpack(   "<ff", self.infile.read(FLOAT*2)) )
        vertexNormal   = ( struct.unpack(  "<fff", self.infile.read(FLOAT*3)) )
        vertexRGBA     = ( struct.unpack( "<BBBB", self.infile.read(UBYTE*4)) )
                    
        if self.debug3:
            print "vertex Pos:",vertexPos
            print "vertex texcoord:",vertexTexcoord
            print "vertex lightmap:",vertexLightmap
            print "vertex normal:", vertexNormal
            print "vertex color:",vertexRGBA

        self.lumpDict["vertices"].append(dict(vertexPos      = vertexPos,
                                              vertexTexcoord = vertexTexcoord,
                                              vertexLightmap = vertexLightmap,
                                              vertexNormal   = vertexNormal,
                                              vertexRGBA     = vertexRGBA))

    def _readVertices(self, offset , length):
        numvertices = length / (3*FLOAT + 2*FLOAT + 2*FLOAT + 3*FLOAT + 4*UBYTE)
        if self.debug:
            print 
            print "START OF VERTEXDATA"
            print "number of numvertices:", numvertices

        self.infile.seek(offset)
        for i in range(0,numvertices):
            if self.debug3: print
            if self.debug2:  print "vertex #", i

            self._readVertex()

        if self.debug:
            print "END OF VERTEXDATA" 

    def _readFace(self):
        texture         =  struct.unpack("<i",   self.infile.read(INT))[0]
        effect          =  struct.unpack("<i",   self.infile.read(INT))[0]
        facetype        =  struct.unpack("<i",   self.infile.read(INT))[0]
        vertex          =  struct.unpack("<i",   self.infile.read(INT))[0]
        nVertices       =  struct.unpack("<i",   self.infile.read(INT))[0]
        meshVertex      =  struct.unpack("<i",   self.infile.read(INT))[0]
        nMeshVerts      =  struct.unpack("<i",   self.infile.read(INT))[0]
        lightmapIndex   =  struct.unpack("<i",   self.infile.read(INT))[0]
        lightmapStart   =  struct.unpack("<ii",  self.infile.read(INT*2))
        lightmapSize    =  struct.unpack("<ii",  self.infile.read(INT*2))
        lightmapOrigin  =  struct.unpack("<fff", self.infile.read(FLOAT*3))
        lightmapVecs    = (struct.unpack("<fff", self.infile.read(FLOAT*3)), 
                           struct.unpack("<fff", self.infile.read(FLOAT*3)))
        normal          =  struct.unpack("<fff", self.infile.read(FLOAT*3))
        patchSize       =  struct.unpack("<ii",  self.infile.read(INT*2))

        self.lumpDict["faces"].append(dict(texture=texture,
                                           effect=effect,
                                           facetype=facetype,
                                           vertex=vertex,
                                           nVertices=nVertices,
                                           meshVertex=meshVertex,
                                           nMeshVerts=nMeshVerts,
                                           lightmapIndex=lightmapIndex,
                                           lightmapStart=lightmapStart,
                                           lightmapSize=lightmapSize,
                                           lightmapOrigin=lightmapOrigin,
                                           lightmapVecs=lightmapVecs,
                                           normal=normal,
                                           patchSize=patchSize))

        if self.debug2:
            print facetype,vertex,nVertices,meshVertex,nMeshVerts

        if self.debug3:
            print 
            print "texture index:",           texture
            print "effect index:",            effect
            print "face type:",               facetype
            print "vertex index:",            vertex
            print "number of vertices:",      nVertices
            print "mesh vertex:",             meshVertex
            print "number of mesh vertices:", nMeshVerts
            print "lightmap index:",          lightmapIndex
            print "lightmap Start:",          lightmapStart
            print "lightmap Size:",           lightmapSize
            print "lightmap Origin:",         lightmapOrigin
            print "lightmap Vectors:",        lightmapVecs
            print "face normal:",             normal
            print "patch size:",              patchSize

    def _readFaces(self, offset, length):
        numfaces = length / (14*INT + 12*FLOAT)
        if self.debug:
            print 
            print "START OF FACEDATA"
            print "number of faces:", numfaces


        self.infile.seek(offset)
        for i in range(numfaces):
            if self.debug3:
                print 
                print "faceNr:" ,i
            self._readFace()

        if self.debug:
            print "END OF FACEDATA"

    def _readEffect(self):
        effectname = self.infile.read(STRING).rstrip("\0")
        brush      = struct.unpack("<i", self.infile.read(INT))[0]
        unknown    = struct.unpack("<i", self.infile.read(INT))[0]

        if self.debug2:
            print
            print "effectname:" , effectname
            print "sourceFlags:", hex(brush) , "contentFlags:",hex(unknown)

        return effectname

    def _readEffects(self, offset, length):
        if self.debug:
            print
            print "START OF EFFECTS"

        numeffect = length/(STRING+INT+INT) # 64 chars, int, int
        if self.debug:
            print "Number of effects", numeffect

        self.infile.seek(offset)
        for i in range(numeffect):
            self.lumpDict["effects"].append(self._readEffect())

        if self.debug:
            print "END OF EFFECTS"

    def _convertEntityType(self, name, value):
        if   name == "origin":     value = self.Vector(map(lambda e: int(e), value))
        elif name == "spawnflags": value = map(lambda e: int(e), value)
        elif name == "random":     value = map(lambda e: int(e), value)
        elif name == "wait":       value = map(lambda e: float(e), value)
        elif name == "light":      value = map(lambda e: int(e), value)
        elif name == "_color":     value = map(lambda e: float(e), value)

        if len(value) == 1:
            value = value[0]

        return name, value

    def _readEntityBlock(self, block):
        eDict = {}
        for line in block.split("\n"):
            if line == "" or line == "}" or len(line) == 1: continue # Ignore empty lines

            lineSplit = line.split()
            name, value = self._convertEntityType(lineSplit.pop(0), lineSplit)

            eDict[name] = value

        self.lumpDict["entities"].append(eDict)

    def _readEntities(self, offset, length):
        if self.debug:
            print
            print "START OF EFFECTS"

        self.infile.seek(offset)
        string = self.infile.read(length).replace("\"","").split("{")
        string.pop(0) # Remove first element, since it will always be empty due to .split("{")
        for block in string:
            self._readEntityBlock(block)

        if self.debug:
            print "END OF EFFECTS"

    def _readModel(self):

        mins      = struct.unpack("<fff", self.infile.read(FLOAT*3))
        maxs      = struct.unpack("<fff", self.infile.read(FLOAT*3))
        face      = struct.unpack("<i",   self.infile.read(INT))[0]
        n_faces   = struct.unpack("<i",   self.infile.read(INT))[0]
        brush     = struct.unpack("<i",   self.infile.read(INT))[0]
        n_brushes = struct.unpack("<i",   self.infile.read(INT))[0]

        if self.debug3:
            print
            print "mins",mins
            print "maxs",maxs
            print "face",face
            print "n_faces", n_faces
            print "brush", brush
            print "n_brushes", n_brushes

        return (mins, maxs, face, n_faces, brush, n_brushes)

    def _readModels(self, offset, length):
        if self.debug:
            print
            print "START OF MODELS"

        nummodels = length/(FLOAT*6+INT*4) # float[3], float[3], int, int, int, int
        if self.debug:
            print "Number of models", nummodels

        self.infile.seek(offset)
        for i in range(nummodels):
            self.lumpDict["models"].append(self._readModel())

        if self.debug:
            print "END OF MODELS"

    def _readBrush(self):
        brushside    = struct.unpack("<i", self.infile.read(INT))[0]
        n_brushsides = struct.unpack("<i", self.infile.read(INT))[0]
        texture      = struct.unpack("<i", self.infile.read(INT))[0]

        if self.debug3:
            print
            print "brushside",brushside
            print "n_brushsides",n_brushsides
            print "texture",texture

        return (brushside, n_brushsides, texture)

    def _readBrushes(self, offset, length):
        if self.debug:
            print
            print "START OF BRUSHES"

        numbrush = length/(INT*3) # int, int, int
        if self.debug:
            print "Number of brushes", numbrush

        self.infile.seek(offset)
        for i in range(numbrush):
            self.lumpDict["brushes"].append(self._readBrush())

        if self.debug:
            print "END OF BRUSHES"

    def _readBrushside(self):
        plane   = struct.unpack("<i", self.infile.read(INT))[0]
        texture = struct.unpack("<i", self.infile.read(INT))[0]

        if self.debug3:
            print
            print "plane",plane
            print "texture",texture

        return (plane, texture)

    def _readBrushsides(self, offset, length):
        if self.debug:
            print
            print "START OF BRUSHESIDES"

        numbrush = length/(INT*2) # int, int
        if self.debug:
            print "Number of brushsides", numbrush

        self.infile.seek(offset)
        for i in range(numbrush):
            self.lumpDict["brushsides"].append(self._readBrushside())

        if self.debug:
            print "END OF BRUSHESIDES"

    def _readPlane(self):
        normal = struct.unpack("<fff", self.infile.read(FLOAT*3))
        dist   = struct.unpack("<f", self.infile.read(FLOAT))[0]

        if self.debug3:
            print
            print "normal",normal
            print "dist",dist

        return (normal, dist)

    def _readPlanes(self, offset, length):
        if self.debug:
            print
            print "START OF PLANES"

        nummodels = length/(FLOAT*3+INT) # float[3], int
        if self.debug:
            print "Number of planes", nummodels

        self.infile.seek(offset)
        for i in range(nummodels):
            self.lumpDict["planes"].append(self._readPlane())

        if self.debug:
            print "END OF PLANES"

    def _readVisdata(self, offset, length):
        self.lumpDict["visdata"].append("not implemented yet")
        """
        if self.debug or True:
            print
            print "START OF VISDATA"

        self.infile.seek(offset)
        n_vecs  = struct.unpack("<i", self.infile.read(4))[0]
        sz_vecs = struct.unpack("<i", self.infile.read(4))[0]
        vec = []

        for n in range(length-4-4):
            vec.append(struct.unpack("<BBB", self.infile.read(3)))

        for v in vec:
            print v

        if self.debug or True:
            print "END OF VISDATA"


        # int n_vecs  Number of vectors.
        # int sz_vecs Size of each vector, in bytes.
        # ubyte[n_vecs * sz_vecs] vecs    Visibility data. One bit per cluster per vector.
        """

    def _readLightvols(self, offset, length):
        self.lumpDict["lightvols"].append("not implemented yet")

    def _readNodes(self, offset, length):
        self.lumpDict["nodes"].append("not implemented yet")

    def _readLeafs(self, offset, length):
        self.lumpDict["leafs"].append("not implemented yet")

    def _readLeafsFaces(self, offset, length):
        self.lumpDict["leaffaces"].append("not implemented yet")

    def _readLeafBrushes(self, offset, length):
        self.lumpDict["leafbrushes"].append("not implemented yet")

if __name__ == "__main__":
    newBSP = BSP('maps/q3tourney6.bsp', vector = GAME_OBJ, gfx = PYGAME)

