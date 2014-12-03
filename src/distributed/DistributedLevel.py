from direct.distributed.DistributedObject import DistributedObject
import random

# 3D-Points
from panda3d.core import Vec3
from panda3d.core import VBase2
from panda3d.core import Point2
from panda3d.core import Point3

# camera
from panda3d.core import LensNode

# collisions
from panda3d.core import Plane
from panda3d.core import BitMask32
from panda3d.core import CollisionPlane
from panda3d.core import CollisionNode
from panda3d.core import CollisionRay
from panda3d.core import CollisionHandlerQueue
from panda3d.core import CollisionTraverser

# Generator
#from generator.builder import Builder


# Distributed Level
class DistributedLevel(DistributedObject):

    """ An instance of these is created and placed in the middle of
    the zone.  It serves to illustrate the creation of AI-side objects
    to populate the world, and a general mechanism for making them
    react to the avatars. """

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        #self.model = loader.loadModel('environment')
        #self.model.setZ(0)
        #self.builder = Builder(self, "map.txt", "development")


        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        cnode = CollisionNode('cnode')
        cnode.setIntoCollideMask(BitMask32.bit(1))
        cnode.setFromCollideMask(BitMask32.bit(1))
        cnode.addSolid(plane)
        self.planeNP = self.model.attachNewNode(cnode)
        self.planeNP.show()

        # Setup a traverser for the picking collisions
        self.picker = CollisionTraverser()
        # Setup mouse ray
        self.pq = CollisionHandlerQueue()
        # Create a collision Node
        pickerNode = CollisionNode('MouseRay')
        # set the nodes collision bitmask
        pickerNode.setFromCollideMask(BitMask32.bit(1))
        # create a collision ray
        self.pickerRay = CollisionRay()
        # add the ray as a solid to the picker node
        pickerNode.addSolid(self.pickerRay)
        # create a nodepath with the camera to the picker node
        self.pickerNP = base.camera.attachNewNode(pickerNode)
        # add the nodepath to the base traverser
        self.picker.addCollider(self.pickerNP, self.pq)

        print "model loaded"
        #TODO: check how to load multiple levels and set players in specific levels!
        self.accept("mouse1", self.mouseClick)

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

    def checkMousePos(self, mpos, camPos, camHpr):
        lens = LenseNode.copyLens(base.camNode)
        lens.setPos(camPos)
        lens.setHpr(camHpr)
        help(mpos)
        mpos = Point2(mpos.x, mpos.y)
        pos = self.getClickPosition(mpos, lens)
        print "mouse clicked at:", pos

    def mouseClick(self):
        """Send an event to the server that will check where the mouse
        will hit and what action needs to be done"""
        hitPos = (0, 0, 0)
        # check if we have a mouse on the window
        if base.mouseWatcherNode.hasMouse():
            # get the mouse position on the screen
            mpos = base.mouseWatcherNode.getMouse()
            print mpos
            # set the ray's position
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            # Now call the traverse function to let the traverser check for collisions
            # with the added colliders and the levelNP
            self.picker.traverse(self.planeNP)
            # check if we have a collision
            if self.pq.getNumEntries() > 0:
                # sort the entries to get the closest first
                self.pq.sortEntries()
                # This is the point at where the mouse ray and the level plane intersect
                hitPos = self.pq.getEntry(0).getSurfacePoint(render)
        base.messenger.send("clickPosition", [hitPos])
