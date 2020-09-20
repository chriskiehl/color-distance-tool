import wx
import wx.lib.mixins.inspection
from colordistance.util import fix

class ColorSwatch(wx.Panel):
    """
    Just a rectangle showing the currently selected color plus
    a minimal amount of additional user feedback to show selection state.
    """

    def __init__(self, parent, *args, **kwargs):
        super(ColorSwatch, self).__init__(parent, *args)
        self.SetSize((75,75))
        self.SetMinSize((75,75))
        self.Bind(wx.EVT_PAINT, self.onPaint)

        self.hovering = False
        self.props = kwargs.pop('props', {
            'selected': False,
            'color': (255, 255, 255),
        })
        self.Refresh()

    def updateProps(self, props):
        self.props = props
        self.Refresh()

    def onPaint(self, event):
        pdc = wx.PaintDC(self)
        gc = wx.GCDC(pdc)
        gc.Clear()

        w,h = self.GetSize()
        gc.SetPen(wx.Pen("", style=wx.PENSTYLE_TRANSPARENT))
        gc.SetBrush(wx.Brush(self.GetBackgroundColour(), style=wx.BRUSHSTYLE_SOLID))
        gc.DrawRectangle(0, 0, w,h)


        gc.SetPen(wx.Pen("rgba(0,0,0,0.7)", 2 if self.props.get('selected', False) else 1))
        gc.SetBrush(wx.Brush(f'rgb{self.props.get("color")}', style=wx.BRUSHSTYLE_SOLID))
        gc.DrawRectangle(3, 3, w - 6, h - 6)


class ColorSelector(wx.Panel):
    """
    Color Picker and various color space details.
    """
    def __init__(self, *args, **kwargs):
        super(ColorSelector, self).__init__(*args)

        self.id = kwargs.pop('id')
        self.swatch = ColorSwatch(self)
        self.button = wx.Button(self, label='Choose color')
        self.rgb = wx.StaticText(self)
        self.lab = wx.StaticText(self)
        self.hsv = wx.StaticText(self)
        self.layout()

        self.Bind(wx.EVT_BUTTON, fix(kwargs.pop('onClick'), self.id), self.button)


    def updateProps(self, colorProps):
        """
        Update the UI components to reflect the latest state.
        """
        for colorSpace in ['rgb', 'lab', 'hsv']:
            color = self.formatColorValues(colorProps.get(colorSpace, '-'))
            getattr(self, colorSpace).SetLabel(f"{colorSpace.upper()}: {color}")
        self.swatch.updateProps(colorProps)

    def formatColorValues(self, color):
        """
        LAB* values can be crazy precise. Truncating
        things for ease of display
        """
        return tuple([float('{0:.4f}'.format(x)) for x in color])

    def layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.swatch, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.button, 0, wx.ALIGN_CENTER_HORIZONTAL)

        sizer.Add(self.rgb, 1, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.lab, 1,wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.hsv, 1, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(sizer)
        self.Layout()


class DifferenceLine(wx.Panel):
    """
    Wrapper component for displaying the distances between selected colors.
    """
    def __init__(self, *args):
        super(DifferenceLine, self).__init__(*args)
        self.props = {'rgb': '-', 'lab': '-'}
        self.diffs = [
            wx.StaticText(self, -1, label='RGB diff: -'),
            wx.StaticText(self, -1, label='LAB diff: -')
        ]
        self.layout()

    def updateProps(self, props):
        self.props = props
        for key, obj in zip(['rgb', 'lab'], self.diffs):
            obj.SetLabel(f"{key.upper()} Diff: {props[key]}")
        self.Refresh()

    def layout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(50)
        vert = wx.BoxSizer(wx.VERTICAL)
        for obj in self.diffs:
            vert.Add(obj, 0)
        sizer.Add(vert)
        self.SetSizer(sizer)