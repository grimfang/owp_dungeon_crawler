from direct.distributed.ServerRepository import ServerRepository
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
