from direct.distributed.DistributedObject import DistributedObject
import random

# Distributed Level
class DistributedLevel(DistributedObject):

    """ An instance of these is created and placed in the middle of
    the zone.  It serves to illustrate the creation of AI-side objects
    to populate the world, and a general mechanism for making them
    react to the avatars. """

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.model = loader.loadModel('environment')
        self.model.setZ(0)
        print "model loaded"

    def announceGenerate(self):
        """ This method is called after generate(), after all of the
        required fields have been filled in.  At the time of this call,
        the distributed object is ready for use. """
        DistributedObject.announceGenerate(self)

        # Now that the object has been fully manifested, we can parent
        # it into the scene.
        print "render the model"
        self.model.reparentTo(render)

    def disable(self):
        # Take it out of the scene graph.
        self.detachNode()

        DistributedObject.disable(self)
