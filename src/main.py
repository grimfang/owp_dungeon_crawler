from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title GrimFang OWP - Dungeon Crawler
    cursor-hidden 0
    show-frame-rate-meter 1
	#win-size 1024 600
    #fullscreen #t
    model-path $MAIN_DIR/assets/
"""
)

from direct.showbase.ShowBase import ShowBase
from gui.MainMenu import MainMenu

class Main(ShowBase):
	"""Main class of the application
	initialise the engine (ShowBase)"""

	def __init__(self):
		"""initialise the engine"""
		ShowBase.__init__(self)
		self.setBackgroundColor(0,0,0)

		self.mainMenu = MainMenu()

		## Basic events
		self.acceptAll()

	def host(self):
		"""starting the server"""
		# instantiate the server
		from server.server import DungeonServerRepository
		self.sr = DungeonServerRepository()
		# instantiate the Level
		from client.client import LevelAIRepository
		print "start the Level AI"
		self.levelAI = LevelAIRepository()

	def join(self, ip):
		from client.client import Client
		self.client = Client(ip)

	def acceptAll(self):
		"""Accept all events that have to be catched by the main class"""
		self.accept("escape", self.quit)
		self.accept("start_server", self.host)
		self.accept("start_client", self.join)


	def quit(self):
		if self.appRunner:
			self.appRunner.stop()
		else:
			exit(0)

# instantiate the engine
base = Main()

# starting the application
if __name__ == '__main__':
    # start the application
    base.run()
