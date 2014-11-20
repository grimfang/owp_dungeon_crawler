from direct.distributed.ServerRepository import ServerRepository
from direct.distributed.ClientRepository import ClientRepository
from pandac.PandaModules import URLSpec

# the main server class
class DungeonServerRepository(ServerRepository):
    """The server repository class"""
    def __init__(self):
        """initialise the server class"""
        # get the port number from the configuration file
        # if it doesn't exist, use 4400 as the default
        tcpPort = base.config.GetInt('server-port', 4400)
        # list of all needed .dc files
        dcFileNames = ['distributed/direct.dc', 'distributed/net.dc']
        # initialise the server on this machine with the
        # port number and the dc filenames
        ServerRepository.__init__(self, tcpPort, dcFileNames = dcFileNames)

class ServerAIRepository(ClientRepository):
    """a small client only for the Server, which holds the AI Classes"""
    def __init__(self):
        dcFileNames = ['distributed/direct.dc', 'distributed/net.dc']

        ClientRepository.__init__(self, dcFileNames = dcFileNames,
                                  dcSuffix = 'AI')

        tcpPort = base.config.GetInt('server-port', 4400)
        url = URLSpec('http://127.0.0.1:%s' % (tcpPort))
        self.connect([url],
                     successCallback = self.connectSuccess,
                     failureCallback = self.connectFailure)

    def connectFailure(self, statusCode, statusString):
        # if the level fails to load, raise an exception
        raise StandardError, statusString

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        print 'Connection established, waiting for server.'
        # now wait until the server sends us the createReady message
        self.acceptOnce('createReady', self.createReady)

    def createReady(self):
        """ Now we're ready to go! """

        # Put the time manager in zone 1 where the clients can find it.
        base.messenger.send("addLog", ["Setup time manager"])
        self.timeManager = self.createDistributedObject(
            className = 'TimeManagerAI', zoneId = 1)
        base.messenger.send("addLog", ["time manager finished"])

        # Put the Level in zone 1 too.
        base.messenger.send("addLog", ["create the level"])
        self.level = self.createDistributedObject(
            className = 'DistributedLevelAI', zoneId = 1)
        base.messenger.send("addLog", ["level finished"])
