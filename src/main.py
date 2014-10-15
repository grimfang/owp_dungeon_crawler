from direct.showbase.ShowBase import ShowBase

class Main(ShowBase):
	"""Main class of the application
	initialise the engine (ShowBase)"""

	def __init__(self):
		"""initialise the engine"""
		ShowBase.__init__(self)
		self.setBackgroundColor(0,0,0)

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

	def join(self):
		from client.client import Client
		self.client = Client("127.0.0.1")

	def acceptAll(self):
		"""Accept all events that have to be catched by the main class"""
		self.accept("escape", self.quit)
		self.accept("f1", self.host)
		self.accept("f2", self.join)


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
