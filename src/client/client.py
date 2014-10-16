# all imports needed by the client
from direct.showbase.DirectObject import DirectObject
from direct.distributed.ClientRepository import ClientRepository
from pandac.PandaModules import URLSpec


class DungeonClientRepository(ClientRepository):
    """the main client repository class"""
    def __init__(self):
        # list of all needed .dc files
        dcFileNames = ['distributed/direct.dc', 'distributed/net.dc']
        # initialise the client repository on this
        # machine with the dc filenames
        ClientRepository.__init__(self, dcFileNames = dcFileNames)


class Client(DirectObject):
    """The main client class, which contains all the logic
    and stuff you can see in the application and handles the
    connection to the server"""
    def __init__(self, ip):
        """ Default constructor for the Clinet class """
        # get the port number from the configuration file
        # if it doesn't exist, use 4400 as the default
        tcpPort = base.config.GetInt('server-port', 4400)
        # get the host name from the configuration file
        # which we want to connect to. If it doesn't exit
        # we use loopback to connect to
        hostname = base.config.GetString('server-host', ip)
        # now build the url from the data given above
        self.url = URLSpec('http://%s:%s' % (hostname, tcpPort))

        # create the Repository for the client
        self.cr = DungeonClientRepository()
        # and finaly try to connect to the server
        self.cr.connect([self.url],
                        successCallback = self.connectSuccess,
                        failureCallback = self.connectFailure)

    def connectFailure(self, statusCode, statusString):
        """ some error occured while try to connect to the server """
        raise Exception('Failed to connect to %s: %s.'
                        % (self.url, statusString))

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        print 'Connection established, waiting for server.'
        # now wait until the server sends us the createReady message
        self.acceptOnce('createReady', self.createReady)

    def createReady(self):
        """ Now we're ready to go! """
        print "server connection done"
        self.player = self.cr.createDistributedObject(
            className = "DistributedPlayer", zoneId = 1)
        #TODO implement all the things


class LevelAIRepository(ClientRepository):
    """a small client only for the Server, which holds the Level model"""
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
        raise StandardError, statusString

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        print "start now"
        self.acceptOnce('createReady', self.createReady)

    def createReady(self):
        """ Now we're ready to go! """
        print "create the level"
        self.level = self.createDistributedObject(
            className = 'DistributedLevelAI', zoneId = 1)
        print "level finished"
