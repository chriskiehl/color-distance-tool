import wx
import wx.lib.mixins.inspection
from pynput import mouse

import core
import screen
from components import ColorSelector, DifferenceLine
from util import assoc


class Application(wx.Frame):
    """
    Entry point for the application.

    This is a quick and dirty tool for grabbing pixel colors
    from any location / program on the the screen and listing their
    values and distances in various color spaces.
    """
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.keyboardListener = None
        self.mouseListener = None

        self.state = {
            'selected': None,
            'left': {'color': (255, 255, 255)},
            'right': {'color': (255, 255, 255)}
        }

        self.leftSwatch = ColorSelector(self, id='left', onClick=self.onStartColorSelection)
        self.rightSwatch = ColorSelector(self, id='right', onClick=self.onStartColorSelection)
        self.difference = DifferenceLine(self)
        self.icon = wx.Icon('icon.PNG', wx.BITMAP_TYPE_PNG)

        self.layout()
        self.updateState(self.state)

    def updateState(self, nextState):
        """
        Update the main component's state and project new views to children.
        """
        # propagate the new info to the children
        self.state = nextState
        for child in [self.leftSwatch, self.rightSwatch]:
            props = nextState[child.id]
            isSelected = nextState['selected'] == child.id
            child.updateProps(assoc(core.colorspaces(props), 'selected', isSelected))
        self.difference.updateProps(core.computeDiff(nextState))

    def onExternalMouseClick(self, x, y, button, pressed):
        """
        Unhooks the external mouse listener when a click is registered.
        """
        if core.isListening(self.state):
            self.stopInputListers()

    def onExternalMouseMove(self, x, y):
        """
        Update the selected swatch with the color found
        at the current mouse coordinates.
        """
        selected = self.state['selected']
        rgb = screen.get_pixel(x, y)
        self.updateState(core.updateColor(self.state, selected, rgb))

    def onStartColorSelection(self, swatchId):
        """
        Select the supplied Swatch and install a global mouse listener.
        """
        self.updateState(core.selectSwatch(self.state, swatchId))
        self.startInputListeners()

    def startInputListeners(self):
        """
        Start a mouse listener on a separate thread.
        """
        if self.mouseListener:
            self.mouseListener.stop()
        # it's got some weird threading setup that
        # requires it to be destroyed / recreated
        self.mouseListener = mouse.Listener(on_click=self.onExternalMouseClick, on_move=self.onExternalMouseMove)
        self.mouseListener.start()

    def stopInputListers(self):
        """
        Shut down the current listener
        """
        self.mouseListener.stop()

    def layout(self):
        self.SetIcon(self.icon)
        self.SetSize(500, 250)
        self.SetBackgroundColour(self.leftSwatch.GetBackgroundColour())
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.leftSwatch, wx.EXPAND)
        sizer.Add(self.rightSwatch, wx.EXPAND)
        v = wx.BoxSizer(wx.VERTICAL)
        v.AddSpacer(10)
        v.Add(sizer, 1, wx.EXPAND)
        v.AddSpacer(10)
        line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        v.Add(line, 0, wx.EXPAND)
        v.Add(self.difference, 1, wx.EXPAND)
        self.SetSizer(v)


def run():
    app = wx.App(False)
    frame = Application(None)
    frame.Show(True)
    app.MainLoop()



if __name__ == '__main__':
    run()