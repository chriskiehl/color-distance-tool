import math
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor, HSLColor, HSVColor

from util import assoc, associn


def colorspaces(swatchInfo):
    """Project the current RGB color to multiple color spaces"""
    r,g,b = swatchInfo['color']
    rgb = sRGBColor(r,g,b, is_upscaled=True)
    return {
        'color': swatchInfo['color'],
        'rgb':(r,g,b),
        'lab': convert_color(rgb, LabColor).get_value_tuple(),
        'hsv': convert_color(rgb, HSVColor).get_value_tuple(),
        'hsl': convert_color(rgb, HSLColor).get_value_tuple(),
    }


def computeDiff(state):
    """Compute the distance between colors in RGB and LAB color spaces"""
    def dist(color1, color2):
        squareDist = sum([math.pow(b - a, 2) for a, b in zip(color1, color2)])
        return math.sqrt(squareDist)

    left = colorspaces(state['left'])
    right = colorspaces(state['right'])

    return {
        'rgb': dist(left['rgb'], right['rgb']),
        'lab': dist(left['lab'], right['lab'])
    }


def selectSwatch(state, swatchId):
    """Select the supplied swatch in a mutually exclusive manner."""
    return assoc(state, 'selected', swatchId)


def isListening(state):
    """
    Check if the input listeners are active by
    whether or not a color chooser is currently actively selected
    """
    return state.get('selected') is not None


def updateColor(state, swatchId, color):
    """Update the supplied swatch's color."""
    return associn(state, [swatchId, 'color'], color)

