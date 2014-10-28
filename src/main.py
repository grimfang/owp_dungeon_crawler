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
from gui.HostMenu import HostMenu
import socket

class Main(ShowBase):
    """Main class of the application
    initialise the engine (ShowBase)"""

    def __init__(self):
        """initialise the engine"""
        ShowBase.__init__(self)
        self.setBackgroundColor(0,0,0)

        self.mainMenu = MainMenu()
        self.hostMenu = HostMenu()
        self.hostMenu.hide()

        ## Basic events
        self.acceptAll()

    def host(self):
        """starting the server"""
        self.hostMenu.show()
        # instantiate the server
        from server.server import DungeonServerRepository
        self.sr = DungeonServerRepository()
        # instantiate the Level
        from client.client import LevelAIRepository
        base.messenger.send("addLog", ["start the Level AI"])
        self.levelAI = LevelAIRepository()
        ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        base.messenger.send("addLog",
            ["Server at: {} - Running - Version 1.0".format(ip)])

    def stopHost(self):
        self.mainMenu.show()
        del self.levelAI
        self.levelAI = None
        del self.sr
        self.sr = None

    def join(self, ip):
        from client.client import Client
        self.client = Client(ip)

    def stopJoin(self):
        #??? self.client.stop()
        pass

    def acceptAll(self):
        """Accept all events that have to be catched by the main class"""
        self.accept("escape", self.quit)
        self.accept("start_server", self.host)
        self.accept("stop_server", self.stopHost)
        self.accept("start_client", self.join)
        self.accept("stop_client", self.stopJoin)


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
