from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectEntry
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import OkDialog
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectCheckBox import DirectCheckBox
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode
from panda3d.core import Vec3

class MainMenu(DirectObject):
    """This class represents the main menu as seen directly after the
    application has been started"""
    def __init__(self):

        # loading music
        self.menuMusic = loader.loadMusic("music/01Menu.mp3")
        self.menuMusic.setLoop(True)

        # create a main frame as big as the window
        self.frameMain = DirectFrame(
            # set framesize the same size as the window
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dTop, base.a2dBottom),
            # position center
            pos = (0, 0, 0),
            # set tramsparent background color
            frameColor = (0.15, 0.15, 0.15, 1))
        #self.frameMain.reparentTo(render2d)

        self.menuBackground = OnscreenImage(
            image = 'gui/Background.png',
            scale = (1.66, 1, 1),
            pos = (0, 0, 0))
        self.menuBackground.reparentTo(self.frameMain)

        self.defaultBtnMap = base.loader.loadModel("gui/button_map")
        self.buttonGeom = (
            self.defaultBtnMap.find("**/button_ready"),
            self.defaultBtnMap.find("**/button_click"),
            self.defaultBtnMap.find("**/button_rollover"),
            self.defaultBtnMap.find("**/button_disabled"))
        self.defaultTxtMap = base.loader.loadModel("gui/textbox_map")
        self.textboxGeom = self.defaultTxtMap.find("**/textbox")

        monospace = loader.loadFont('gui/DejaVuSansMono.ttf')
        defaultFont = loader.loadFont('gui/eufm10.ttf')

        # create the title
        self.textscale = 0.25
        self.title = DirectLabel(
            # scale and position
            scale = self.textscale,
            pos = (0.0, 0.0, base.a2dTop - self.textscale),
            # frame
            frameColor = (0, 0, 0, 0),
            # Text
            text = "Dungeon Crawler",
            text_align = TextNode.ACenter,
            text_fg = (0.82,0.85,0.87,1),
            text_shadow = (0, 0, 0, 1),
            text_shadowOffset = (-0.02, -0.02),
            text_font = defaultFont)
        self.title.setTransparency(1)
        self.title.reparentTo(self.frameMain)

        # create a host button
        self.btnHostPos = Vec3(0, 0, .45)
        self.btnHostScale = 0.25
        self.btnHost = DirectButton(
            # Scale and position
            scale = self.btnHostScale,
            pos = self.btnHostPos,
            # Text
            text = "Host",
            text_scale = 0.8,
            text_pos = (0, -0.2),
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
            command = self.host,
            rolloverSound = None,
            clickSound = None)
        self.btnHost.setTransparency(1)
        self.btnHost.reparentTo(self.frameMain)

        # create a join button
        self.btnJoinPos = Vec3(0, 0, 0)
        self.btnJoinScale = 0.25
        self.btnJoin = DirectButton(
            scale = self.btnJoinScale,
            pos = self.btnJoinPos,
            text = "Join",
            text_scale = 0.8,
            text_pos = (0, -0.2),
            text_fg = (0.82,0.85,0.87,1),
            text_shadow = (0, 0, 0, 1),
            text_shadowOffset = (-0.02, -0.02),
            text_font = defaultFont,
            geom = self.buttonGeom,
            frameColor = (0, 0, 0, 0),
            relief = 0,
            pressEffect = False,
            command = self.join,
            rolloverSound = None,
            clickSound = None)
        self.btnJoin.setTransparency(1)
        self.btnJoin.reparentTo(self.frameMain)

        # create the IP input field
        self.txtIPPos = Vec3(0, 0, -.30)
        self.txtIPScale = 0.25
        self.txtIPWidth = 9
        self.txtIP = DirectEntry(
            # scale and position
            pos = self.txtIPPos,
            scale = self.txtIPScale,
            width = self.txtIPWidth,
            # Text
            entryFont = monospace,
            text_align = TextNode.ACenter,
            text = "",
            text_scale = 0.5,
            text_pos = (0, -0.2),
            text_fg = (0.82,0.85,0.87,1),
            text_shadow = (0, 0, 0, 1),
            text_shadowOffset = (0.04, 0.04),
            initialText = "127.0.0.1",
            numLines = 1,
            # Frame
            geom = self.textboxGeom,
            frameColor = (0, 0, 0, 0),
            relief = 0,
            # Functionality
            command = self.join,
            focusInCommand = self.clearText)
        self.txtIP.reparentTo(self.frameMain)

        # create an exit button
        self.btnExitPos = Vec3(0, 0, -.75)
        self.btnExitScale = 0.25
        self.btnExit = DirectButton(
            scale = self.btnExitScale,
            pos = self.btnExitPos,
            text = "Exit",
            text_scale = 0.8,
            text_pos = (0, -0.2),
            text_fg = (0.82,0.85,0.87,1),
            text_shadow = (0, 0, 0, 1),
            text_shadowOffset = (-0.02, -0.02),
            text_font = defaultFont,
            geom = self.buttonGeom,
            frameColor = (0, 0, 0, 0),
            relief = 0,
            pressEffect = False,
            command = lambda: base.messenger.send("escape"),
            rolloverSound = None,
            clickSound = None)
        self.btnExit.setTransparency(1)
        self.btnExit.reparentTo(self.frameMain)

        # create a mute checkbox
        self.cbVolumeMute = DirectCheckBox(
            # set size
            scale = (0.1, 0.1, 0.1),
            frameSize = (-1, 1, 1, -1),
            # functionality and visuals
            command = self.cbVolumeMute_CheckedChanged,
            isChecked = True,
            checkedImage = "gui/SoundSwitch_off.png",
            uncheckedImage = "gui/SoundSwitch_on.png",
            # mouse behaviour
            relief = 0,
            pressEffect = False,
            rolloverSound = None,
            clickSound = None
            )
        self.cbVolumeMute.setTransparency(1)
        self.cbVolumeMute.reparentTo(self.frameMain)
        self.cbVolumeMute.commandFunc(None)

        # catch window resizes and recalculate the aspectration
        self.accept("window-event", self.recalcAspectRatio)
        self.accept("showerror", self.showError)

        # show the menu right away
        self.show()

    def host(self):
        """Function which will be called by pressing the host button"""
        self.hide()
        base.messenger.send("start_server")

    def join(self, ip=None):
        """Function which will be called by pressing the join button"""
        if ip == None: ip = self.txtIP.get(True)
        if ip == "": return
        self.hide()
        base.messenger.send("start_client", [ip])

    def showError(self, msg):
        self.show()
        self.dialog = OkDialog(
            dialogName="ErrorDialog",
            text="Error: {}".format(msg),
            command=self.closeDialog)

    def closeDialog(self, args):
        self.dialog.hide()

    def show(self):
        """Show the GUI"""
        self.frameMain.show()
        self.menuMusic.play()

    def hide(self):
        """Hide the GUI"""
        self.frameMain.hide()
        self.menuMusic.stop()

    def clearText(self):
        """Function to clear the text that was previously entered in the
        IP input field"""
        self.txtIP.enterText("")

    def cbVolumeMute_CheckedChanged(self, checked):
        if bool(checked):
            base.disableAllAudio()
        else:
            base.enableAllAudio()

    def recalcAspectRatio(self, window):
        """get the new aspect ratio to resize the mainframe"""
        # set the mainframe size to the window borders again
        self.frameMain["frameSize"] = (
            base.a2dLeft, base.a2dRight,
            base.a2dTop, base.a2dBottom)

        # calculate new aspec tratio
        wp = window.getProperties()
        aspX = 1.0
        aspY = 1.0
        wpXSize = wp.getXSize()
        wpYSize = wp.getYSize()
        if wpXSize > wpYSize:
            aspX = wpXSize / float(wpYSize)
        else:
            aspY = wpYSize / float(wpXSize)
        # calculate new position/size/whatever of the gui items
        self.title.setPos(0.0, 0.0, base.a2dTop - self.textscale)
        self.menuBackground.setScale(1.0 * aspX, 1.0, 1.0 * aspY)
        self.cbVolumeMute.setPos(base.a2dRight - 0.15, 0, base.a2dBottom + 0.15)

