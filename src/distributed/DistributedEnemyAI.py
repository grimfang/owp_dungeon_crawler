from direct.distributed.DistributedObjectAI import DistributedObjectAI

# Distributed Enemy AI
class DistributedEnemyAI(DistributedObjectAI):

    """ This is the AI-side implementation of DistributedEnemy. """

    def __init__(self, cr):
        DistributedObjectAI.__init__(self, cr)
