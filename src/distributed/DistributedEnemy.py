from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from pandac.PandaModules import NodePath

# Distributed Enemy
class DistributedEnemy(DistributedSmoothNode):
    def __init__(self, cr):
        DistributedSmoothNode.__init__(self, cr)
        NodePath.__init__(self, "Model")
        self.model = base.loader.loadModel('smiley.egg')
        self.model.reparentTo(self)
        #TODO: setup basic AI system with PandAI

    def generate(self):
        DistributedSmoothNode.generate(self)
        self.activateSmoothing(True, False)
        self.startSmooth()

    def announceGenerate(self):
        DistributedSmoothNode.announceGenerate(self)
        self.reparentTo(base.render)

    def disable(self):
        self.stopSmooth()
        self.model.detachNode()
        DistributedSmoothNode.disable(self)

    def delete(self):
        self.model = None
        DistributedSmoothNode.delete(self)
