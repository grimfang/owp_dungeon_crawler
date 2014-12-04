# Config for the builder
import sys
import os
import ConfigParser

TILESETS = {}
MAPFILENAME = "map.txt"


### TILESET LOADER ###
tilesetsCfg = ConfigParser.RawConfigParser()
tilesetsCfg.read('tilesets.cfg')


def updateTilesets():
	idx = 0
	for section in tilesetsCfg.sections():
		TILESETS[idx] = dict(tilesetsCfg.items(section))
		idx += 1
		print section