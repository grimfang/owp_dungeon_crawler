

# Dungeon builder.
# this should be shared between the client and the server... 
# the only server side part is the generator.py that makes the map.txt file
# passes it to the clients so that they could build it.
# The server builds its own stripped down version.

## SYSTEM IMPORTS ##
import random
#import direct.directbase.DirectStart
from panda3d.core import *
#from BlenderMeshGen import MyApp

# Generator
import config

#------------------------------------------#
# Builder
# Build the 3d level from the generated '2d', map.txt 
#   (networked: map.txt supplied from the server)
# Would be nice to be able to save maps... Could have the server generate,
# map files when ever it has time to spare, or when its on high demand ofc.. 
# But in a smart way...
#-------------------------------------------#

class Builder():

	def __init__(self, _DLAI, _mapFile, _name, _size='normal'): # small, normal, large, huge...

		self.mapFile = _mapFile
		self.mapName = _name
		self.size = _size
		self.grid = {}

		# temp
		self.levelFloor = None
		self.levelFull = None

		config.updateTilesets()
		#self.tileset = self.getRandomTileset()
		self.parseMapFile()
		self.levelNP = self.placeTiles()

		# gen
		#self.generateNavMesh()

		# Testing light
		dlight = DirectionalLight("test")
		dlnp = render.attachNewNode(dlight)
		dlnp.setHpr(180, -20, 0)
		render.setLight(dlnp)


	def generateNavMesh(self):
		MyApp(self.levelFull, self.levelFloor)


	def placeTiles(self):

		# Nodes
		self.levelFull = render.attachNewNode("levelFull")
		self.levelFloor = render.attachNewNode("levelFloor")

		tileSolidModel = self.tileset['solid']
		tileFloorModel = self.tileset['floor']
		tilePortalModel = self.tileset['portal']
		tileSolid = loader.loadModel(tileSolidModel)
		tileFloor = loader.loadModel(tileFloorModel)
		tilePortal = loader.loadModel(tilePortalModel)
		tileSolid.reparentTo(self.levelFull)
		tileFloor.reparentTo(self.levelFloor)
		tilePortal.reparentTo(render)
		
		for y in self.grid:
			for x in self.grid[y]:
				#print self.grid[y][x], "@ position: ", y,x

				if self.grid[y][x] == "x":
					pass

				elif self.grid[y][x] == "#":
					#tileModel = self.tileset['solid']
					#tile = loader.loadModel(tileModel)
					tileSolid.copyTo(self.levelFull)
					tileSolid.setPos(y, x, 0)

				elif self.grid[y][x] == ".":
					#tileModel = self.tileset['floor']
					#tile = loader.loadModel(tileModel)
					tileFloor.copyTo(self.levelFloor)
					tileFloor.setPos(y, x, 0)

				elif self.grid[y][x] == "<" or self.grid[y][x] == ">":
					#tileModel = self.tileset['portal']
					#tile = loader.loadModel(tileModel)
					tilePortal.copyTo(render) #reparentTo(render)
					tilePortal.setPos(y, x, 0)

		
		#self.levelFloor.node().combineWith(self.levelFull.node())
		x = self.levelFloor.output
		print x #render.ls()

		return self.levelFull



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
		print "TILES", config.TILESETS
		tileIndex = random.choice(range(0, len(config.TILESETS)))
		return config.TILESETS[tileIndex]




#builder = Builder("self", "map.txt", "testing")



#run()



