"""
===========================================================================
Copyright (C) 1999-2005 Id Software, Inc.

This file is part of Quake III Arena source code.

Quake III Arena source code is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

Quake III Arena source code is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
===========================================================================


Translated into Python by Troels Ynddal (24. March 2014)
"""


# This file must be identical in the quake and utils directories

# contents flags are seperate bits
# a given brush can contribute multiple content bits

# these definitions also need to be in q_shared.h!

CONTENTS_SOLID          = 1       # an eye is never valid in a solid
CONTENTS_LAVA           = 8
CONTENTS_SLIME          = 16
CONTENTS_WATER          = 32
CONTENTS_FOG            = 64

CONTENTS_AREAPORTAL     = 0x8000

CONTENTS_PLAYERCLIP     = 0x10000
CONTENTS_MONSTERCLIP    = 0x20000
# bot specific contents types
CONTENTS_TELEPORTER     = 0x40000
CONTENTS_JUMPPAD        = 0x80000
CONTENTS_CLUSTERPORTAL  = 0x100000
CONTENTS_DONOTENTER     = 0x200000

CONTENTS_ORIGIN         = 0x1000000   # removed before bsping an entity

CONTENTS_BODY           = 0x2000000   # should never be on a brush, only in game
CONTENTS_CORPSE         = 0x4000000
CONTENTS_DETAIL         = 0x8000000   # brushes not used for the bsp
CONTENTS_STRUCTURAL     = 0x10000000  # brushes used for the bsp
CONTENTS_TRANSLUCENT    = 0x20000000  # don't consume surface fragments inside
CONTENTS_TRIGGER        = 0x40000000
CONTENTS_NODROP         = 0x80000000  # don't leave bodies or items (death fog, lava)

SURF_NODAMAGE           = 0x1     # never give falling damage
SURF_SLICK              = 0x2     # effects game physics
SURF_SKY                = 0x4     # lighting from environment map
SURF_LADDER             = 0x8
SURF_NOIMPACT           = 0x10    # don't make missile explosions
SURF_NOMARKS            = 0x20    # don't leave missile marks
SURF_FLESH              = 0x40    # make flesh sounds and effects
SURF_NODRAW             = 0x80    # don't generate a drawsurface at all
SURF_HINT               = 0x100   # make a primary bsp splitter
SURF_SKIP               = 0x200   # completely ignore, allowing non-closed brushes
SURF_NOLIGHTMAP         = 0x400   # surface doesn't need a lightmap
SURF_POINTLIGHT         = 0x800   # generate lighting info at vertexes
SURF_METALSTEPS         = 0x1000  # clanking footsteps
SURF_NOSTEPS            = 0x2000  # no footstep sounds
SURF_NONSOLID           = 0x4000  # don't collide against curves with this set
SURF_LIGHTFILTER        = 0x8000  # act as a light filter during q3map -light
SURF_ALPHASHADOW        = 0x10000 # do per-pixel light shadow casting in q3map
SURF_NODLIGHT           = 0x20000 # never add dynamic lights


