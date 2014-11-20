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
        # send a message, that should show the client the error message
        base.messenger.send(
            "showerror",
            ["Failed to connect to %s: %s." % (self.url, statusString)])

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        print "Connection established, waiting for server."
        self.cr.setInterestZones([1])
        self.acceptOnce('gotTimeSync', self.syncReady)

    def syncReady(self):
        """ Now we've got the TimeManager manifested, and we're in
        sync with the server time. Now we can enter the world. Check
        to see if we've received our doIdBase yet. """
        if self.cr.haveCreateAuthority():
            self.createReady()
        else:
            # Not yet, keep waiting a bit longer.
            self.acceptOnce('createReady', self.createReady)

    def createReady(self):
        """ Now we're ready to go! """
        print "server connection done"
        self.player = self.cr.createDistributedObject(
            className = "DistributedPlayer", zoneId = 1)

        self.player.startPosHprBroadcast()

        # Unsure?? This maybe a good place to run a precheck to get
        # everything ready or something like that :P
        self.accept("clickPosition", self.walkTo)

    def walkTo(self, pos):
        self.player.lookAt(pos)
        #moveInterval = self.model.posInterval(1, pos)
        #moveInterval.start()
        self.player.setPos(pos)
