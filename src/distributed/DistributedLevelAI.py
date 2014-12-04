from direct.distributed.DistributedObjectAI import DistributedObjectAI



# Distributed Level AI
class DistributedLevelAI(DistributedObjectAI):

    """ This is the AI-side implementation of DistributedLevel. """

    def __init__(self, cr):
        DistributedObjectAI.__init__(self, cr)
        base.messenger.send("addLog", ["Distributed Level AI initialised"])

        