from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionNode
from panda3d.core import CollisionRay
from panda3d.core import BitMask32
from panda3d.core import CollisionHandlerQueue
from panda3d.core import CollisionTraverser
from panda3d.core import Point3

class Mouse(DirectObject):
    def __init__(self):
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

    def setCollisionNp(self, collisionNP):
        """This method has to be called to store the nodepath to the
        collision solid which should be used to check for intersections
        with the mouse ray"""
        self.collisionNP = collisionNP

    def getMousePos(self):
        """Returns the point on the given collision solid where the
        mouse ray will hit"""
        # check if we have a mouse on the window
        if base.mouseWatcherNode.hasMouse():
            # get the mouse position on the screen
            mpos = base.mouseWatcherNode.getMouse()
            # set the ray's position
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            # Now call the traverse function to let the traverser check for collisions
            # with the added colliders and the levelNP
            self.picker.traverse(self.collisionNP)
            # check if we have a collision
            if self.pq.getNumEntries() > 0:
                # sort the entries to get the closest first
                self.pq.sortEntries()
                # This is the point at where the mouse ray and the level plane intersect
                hitPos = self.pq.getEntry(0).getSurfacePoint(render)
                return hitPos
        return Point3(0, 0, 0)

