
# https://www.panda3d.org/forums/viewtopic.php?t=7920
# http://www.mralligator.com/q3/
# https://pypi.python.org/pypi/gameobjects
# http://www.pygame.org/download.shtml

import pygame
import struct
from gameobjects.vector3 import *

DEBUG  = False # 1. level of detail
DEBUG2 = False # 2. level of detail
DEBUG3 = False # 3. level of detail

class BSP(object):
    def __init__(self, fname):
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

        self._readHeader()
        self._readLumps()

        # Read data from lumps
        for lump in self.lumps:
            lump[1](*lump[2])

    def get(self, dictName):
        try:
            return self.lumpDict[dictName]
        except KeyError, e:
            raise Exception("No lump found with that name")
        except:
            raise

    def _readHeader(self):
        if DEBUG:
            print
            print "START OF HEADER"

        magic = self.infile.read(4)
        versionnumber = struct.unpack("<i" , self.infile.read(4))[0]

        if magic != "IBSP": raise Exception("Target file is not a IBSP file")
        if versionnumber != 0x2e: raise Exception("Expected IBSP version be: 0x2e")

        if DEBUG:
            print "magic number:", magic
            print "version number" , hex(versionnumber)
            print "END OF HEADER"
            print

    def _readLumps(self):
        if DEBUG: print "START OF LUMPS"

        for lump in self.lumps:
            if DEBUG: print lump[0]+" lump", 
            lump[2] = self._readLumpEntry()

        if DEBUG: print "END OF LUMPS"
  
    def _readLumpEntry(self):
        lumpEntry = ( struct.unpack("<ii", self.infile.read(4*2)) )
        if DEBUG:
            print lumpEntry

        return lumpEntry

    def _readTexture(self, offset):
        self.infile.seek(offset)
        texturename = self.infile.read(64).rstrip("\0")
        sourceFlags = struct.unpack("<i", self.infile.read(4))[0]
        contentFlags= struct.unpack("<i", self.infile.read(4))[0]

        return (texturename, hex(sourceFlags), hex(contentFlags))

        if DEBUG2:
            print
            print "texturename:" , texturename
            print "sourceFlags:", hex(sourceFlags) , "contentFlags:",hex(contentFlags)

    def _readTextures(self, offset, length):
        if DEBUG:
            print
            print "START OF TEXTURES"

        numtextures = length/(64+4+4) #thats 64chars,4byte int, 4 byte int  
        if DEBUG:
            print "Number of Textures", numtextures
        for i in range(0, numtextures):
            self.lumpDict["textures"].append(self._readTexture(offset+ i*(64+4+4)))

        if DEBUG2:
            for t in self.lumpDict["textures"]:
                print t

        if DEBUG:
            print "END OF TEXTURES"

    def _readLightmap(self, offset):
        width  = 128
        height = 128
        self.infile.seek(offset)

        texture   = pygame.Surface((width,height))
        surfarray = pygame.surfarray.pixels3d(texture)

        for x in range(width):
            for y in range(height):
                surfarray[y][x] = struct.unpack("<BBB", self.infile.read(3))

        pygame.surfarray.blit_array(texture, surfarray)
        self.lumpDict["lightmaps"].append(texture)

    def _readLightmaps(self, offset, length):
        numLightmaps = length/(128*128*3)
        if DEBUG:
            print
            print "START OF LIGHTMAPS"
            print "Number of Lightmaps", numLightmaps

        for i in range(numLightmaps):
            self._readLightmap(offset+ i*(128*128*3) )

        if DEBUG:
            print "END OF LIGHTMAPS"

    def _readMeshverts(self, offset, length):
        self.infile.seek(offset)
        numMeshverts = length/4

        if DEBUG:
            print 
            print "START OF MESHVERTS"
            print "number of meshVertices:", numMeshverts
            print "END OF MESHVERTS"

        for i in range(0,numMeshverts):
            self.lumpDict["meshverts"].append(struct.unpack("<i", self.infile.read(4))[0])

        if DEBUG3:
            for m in self.meshVertsList:
                print m

    def _readVertex(self, offset):
        self.infile.seek(offset)
        vertexPos      = ( struct.unpack(  "<fff", self.infile.read(4*3)) )
        vertexTexcoord = ( struct.unpack(   "<ff", self.infile.read(4*2)) )
        vertexLightmap = ( struct.unpack(   "<ff", self.infile.read(4*2)) )
        vertexNormal   = ( struct.unpack(  "<fff", self.infile.read(4*3)) )
        vertexRGBA     = ( struct.unpack( "<BBBB", self.infile.read(1*4)) )
                    
        if DEBUG3:
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
        numvertices = length / ( 3*4 + 2*4 + 2*4 + 3*4 + 4*1)
        if DEBUG:
            print 
            print "START OF VERTEXDATA"
            print "number of numvertices:", numvertices

        for i in range(0,numvertices):
            if DEBUG3: print
            if DEBUG2:  print "vertex #", i

            self._readVertex(offset+ i* ( 3*4 + 2*4 + 2*4 + 3*4 + 4*1) )

        if DEBUG:
            print "END OF VERTEXDATA" 

    def _readFace(self, offset):
        self.infile.seek(offset)
    
        texture         =  struct.unpack("<i",   self.infile.read(4))[0]
        effect          =  struct.unpack("<i",   self.infile.read(4))[0]
        facetype        =  struct.unpack("<i",   self.infile.read(4))[0]
        vertex          =  struct.unpack("<i",   self.infile.read(4))[0]
        nVertices       =  struct.unpack("<i",   self.infile.read(4))[0]
        meshVertex      =  struct.unpack("<i",   self.infile.read(4))[0]
        nMeshVerts      =  struct.unpack("<i",   self.infile.read(4))[0]
        lightmapIndex   =  struct.unpack("<i",   self.infile.read(4))[0]
        lightmapStart   =  struct.unpack("<ii",  self.infile.read(4*2))
        lightmapSize    =  struct.unpack("<ii",  self.infile.read(4*2))
        lightmapOrigin  =  struct.unpack("<fff", self.infile.read(4*3))
        lightmapVecs    = (struct.unpack("<fff", self.infile.read(4*3)), 
                           struct.unpack("<fff", self.infile.read(4*3)))
        normal          =  struct.unpack("<fff", self.infile.read(4*3))
        patchSize       =  struct.unpack("<ii",  self.infile.read(4*2))

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

        if DEBUG2:
            print facetype,vertex,nVertices,meshVertex,nMeshVerts

        if DEBUG3:
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
        numfaces = length / (12*4 + 12*4+2*4) 
        if DEBUG:
            print 
            print "START OF FACEDATA"
            print "number of faces:", numfaces

        for i in range(numfaces):
            if DEBUG3:
                print 
                print "faceNr:" ,i
            self._readFace(offset+ i* (12*4 + 12*4+2*4) )

        if DEBUG:
            print "END OF FACEDATA"

    def _readEffect(self, offset):
        self.infile.seek(offset)
        effectname = self.infile.read(64).rstrip("\0")
        brush      = struct.unpack("<i", self.infile.read(4))[0]
        unknown    = struct.unpack("<i", self.infile.read(4))[0]

        return effectname

        if DEBUG2:
            print
            print "effectname:" , effectname
            print "sourceFlags:", hex(brush) , "contentFlags:",hex(unknown)

    def _readEffects(self, offset, length):
        if DEBUG:
            print
            print "START OF EFFECTS"

        numeffect = length/(64+4+4) # 64 chars, 4byte int, 4 byte int
        if DEBUG:
            print "Number of effects", numeffect
        for i in range(numeffect):
            self.lumpDict["effects"].append(self._readEffect(offset+ i*(64+4+4) ))

        if DEBUG2:
            for t in lumpDict["effects"]:
                print t

        if DEBUG:
            print "END OF EFFECTS"

    def _convertEntityType(self, name, value):
        if   name == "origin":     value = Vector3(map(lambda e: int(e), value))
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
        if DEBUG:
            print
            print "START OF EFFECTS"

        self.infile.seek(offset)
        string = self.infile.read(length).replace("\"","").split("{")
        string.pop(0) # Remove first element, since it will always be empty due to .split("{")
        for block in string:
            self._readEntityBlock(block)

        if DEBUG2:
            for e in self.get("entities"):
                print e

        if DEBUG:
            print "END OF EFFECTS"

    def _readVisdata(self, offset, length):
        pass

    def _readLightvols(self, offset, length):
        pass

    def _readPlanes(self, offset, length):
        pass

    def _readNodes(self, offset, length):
        pass

    def _readLeafs(self, offset, length):
        pass

    def _readLeafsFaces(self, offset, length):
        pass

    def _readLeafBrushes(self, offset, length):
        pass

    def _readModel(self, offset):
        self.infile.seek(offset)
        mins      = struct.unpack("<fff", self.infile.read(4*3))
        maxs      = struct.unpack("<fff", self.infile.read(4*3))
        face      = struct.unpack("<i",   self.infile.read(4))[0]
        n_faces   = struct.unpack("<i",   self.infile.read(4))[0]
        brush     = struct.unpack("<i",   self.infile.read(4))[0]
        n_brushes = struct.unpack("<i",   self.infile.read(4))[0]

        if DEBUG3:
            print
            print "mins",mins
            print "maxs",maxs
            print "face",face
            print "n_faces", n_faces
            print "brush", brush
            print "n_brushes", n_brushes

        return (mins, maxs, face, n_faces, brush, n_brushes)

    def _readModels(self, offset, length):
        if DEBUG:
            print
            print "START OF MODELS"

        nummodels = length/(4*3+4*3+4+4+4+4) # 64 chars, 4byte int, 4 byte int
        if DEBUG:
            print "Number of models", nummodels

        for i in range(nummodels):
            self.lumpDict["models"].append(self._readModel(offset+ i*(4*3+4*3+4+4+4+4) ))

        if DEBUG2:
            for model in self.get("models"):
                print model

        if DEBUG:
            print "END OF MODELS"

    def _readBrushes(self, offset, length):
        if DEBUG:
            print
            print "START OF BRUSHES"

        nummodels = length/(4*3+4*3+4+4+4+4) # 64 chars, 4byte int, 4 byte int
        if DEBUG:
            print "Number of brushes", nummodels

        for i in range(nummodels):
            self.lumpDict["brushes"].append(self._readModel(offset+ i*(4*3+4*3+4+4+4+4) ))

        if DEBUG2:
            for model in self.get("brushes"):
                print model

        if DEBUG:
            print "END OF BRUSHES"

    def _readBrushsides(self, offset, length):
        pass


if __name__ == "__main__":
    newBSP = BSP('maps/q3tourney6.bsp')

    pygame.init()
    """
    screenResolution = (640,480)
    screen = pygame.display.set_mode(screenResolution,0,32)
    background = pygame.Surface(screenResolution)
    background.fill((255,255,255))
    clock = pygame.time.Clock()
    loop = True
    while loop:
        time_passed = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    loop = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    loop = False
    
        screen.blit(background,(0,0))

        screen.blit(newBSP.lumpDict["lightmaps"][0], (0,0))
        screen.blit(newBSP.lumpDict["lightmaps"][1], (129,0))
        screen.blit(newBSP.lumpDict["lightmaps"][2], (258,0))
        screen.blit(newBSP.lumpDict["lightmaps"][3], (387,0))
        pygame.display.flip()
    """

