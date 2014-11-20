from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectScrolledFrame
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode
from panda3d.core import Vec3

class HostMenu(DirectObject):
    def __init__(self):
        self.defaultBtnMap = base.loader.loadModel("gui/button_map")
        self.buttonGeom = (
            self.defaultBtnMap.find("**/button_ready"),
            self.defaultBtnMap.find("**/button_click"),
            self.defaultBtnMap.find("**/button_rollover"),
            self.defaultBtnMap.find("**/button_disabled"))

        defaultFont = loader.loadFont('gui/eufm10.ttf')

        self.logFrame = DirectScrolledFrame(
            canvasSize = (0, base.a2dRight * 2, -5, 0),
            frameSize = (0, base.a2dRight * 2,
                (base.a2dBottom+.2) * 2, 0),
            frameColor = (0.1, 0.1, 0.1, 1))
        self.logFrame.reparentTo(base.a2dTopLeft)

        # create the info and server debug output
        self.textscale = 0.1
        self.txtinfo = OnscreenText(
            scale = self.textscale,
            pos = (0.1, -0.1),
            text = "",
            align = TextNode.ALeft,
            fg = (0.1,1.0,0.15,1),
            bg = (0, 0, 0, 0),
            shadow = (0, 0, 0, 1),
            shadowOffset = (-0.02, -0.02))
        self.txtinfo.setTransparency(1)
        self.txtinfo.reparentTo(self.logFrame.getCanvas())

        # create a close Server button
        self.btnBackPos = Vec3(0.4, 0, 0.2)
        self.btnBackScale = 0.25
        self.btnBack = DirectButton(
            # Scale and position
            scale = self.btnBackScale,
            pos = self.btnBackPos,
            # Text
            text = "Quit Server",
            text_scale = 0.45,
            text_pos = (0, -0.1),
            text_fg = (0.82,0.85,0.87,1),
            text_shadow = (0, 0, 0, 1),
            text_shadowOffset = (-0.02, -0.02),
            text_font = defaultFont,
            # Frame
            geom = self.buttonGeom,
            frameColor = (0, 0, 0, 0),
            relief = 0,
            pressEffect = False,
            # Functionality
            command = self.back,
            rolloverSound = None,
            clickSound = None)
        self.btnBack.setTransparency(1)
        self.btnBack.reparentTo(base.a2dBottomLeft)

        # catch window resizes and recalculate the aspectration
        self.accept("window-event", self.recalcAspectRatio)
        self.accept("addLog", self.addLog)

    def show(self):
        self.logFrame.show()
        self.btnBack.show()

    def hide(self):
        self.logFrame.hide()
        self.btnBack.hide()

    def back(self):
        self.hide()
        base.messenger.send("stop_server")
        self.addLog("Quit Server!")

    def addLog(self, text):
        self.txtinfo.appendText(text + "\n")
        textbounds = self.txtinfo.getTightBounds()
        self.logFrame["canvasSize"] = (0, textbounds[1].getX(),
                                        textbounds[0].getZ(), 0)

    def recalcAspectRatio(self, window):
        """get the new aspect ratio to resize the mainframe"""
        # set the mainframe size to the window borders again
        self.logFrame["frameSize"] = (
            0, base.a2dRight * 2,
            (base.a2dBottom+.2) * 2, 0)
        #self.btnBack.setPos(Vec3(0.4, 0, 0.2))
        #self.btnBack.setPos(Vec3(-0.8, 0, -0.6))
