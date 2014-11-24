

# Dungeon builder.
# this should be shared between the client and the server... 
# the only server side part is the generator.py that makes the map.txt file
# passes it to the clients so that they could build it.
# The server builds its own stripped down version.

## SYSTEM IMPORTS ##
import random
import direct.directbase.DirectStart
from panda3d.core import *

# Generator
from config import TILESETS

#------------------------------------------#
# Builder
# Build the 3d level from the generated '2d', map.txt 
#   (networked: map.txt supplied from the server)
#-------------------------------------------#

class Builder():

	def __init__(self, _mapFile, _name, _size='normal'): # small, normal, large, huge...

		self.mapFile = _mapFile
		self.mapName = _name
		self.size = _size
		self.grid = {}

		self.tileset = self.getRandomTileset()
		self.parseMapFile()
		self.placeTiles()

		# Testing light
		dlight = DirectionalLight("test")
		dlnp = render.attachNewNode(dlight)
		dlnp.setHpr(180, -20, 0)
		render.setLight(dlnp)


	def placeTiles(self):
		
		for y in self.grid:
			for x in self.grid[y]:
				#print self.grid[y][x], "@ position: ", y,x

				if self.grid[y][x] == "x":
					pass

				elif self.grid[y][x] == "#":
					tileModel = self.tileset['solid']
					tile = loader.loadModel(str(tileModel.strip("\"")))
					tile.reparentTo(render)
					tile.setPos(y, x, 0)

				elif self.grid[y][x] == ".":
					tileModel = self.tileset['floor']
					tile = loader.loadModel(str(tileModel.strip("\"")))
					tile.reparentTo(render)
					tile.setPos(y, x, 0)

				elif self.grid[y][x] == "<" or self.grid[y][x] == ">":
					tileModel = self.tileset['portal']
					tile = loader.loadModel(str(tileModel.strip("\"")))
					tile.reparentTo(render)
					tile.setPos(y, x, 0)


	def parseMapFile(self):
		lines = []
		with open(self.mapFile) as f:
			lines = [list(line.rstrip()) for line in f]
			f.close()
			
		y = 0
		for line in lines:
			self.grid[y] = {}
			x = 0
			for tile in line:
				self.grid[y][x] = tile
				x += 1

			y += 1
			

	def getRandomTileset(self):
		tileIndex = random.choice(range(len(TILESETS)))
		return TILESETS[tileIndex]




builder = Builder("map.txt", "testing")



run()



