from ctypes import *

user32 = windll.user32
gdi = windll.gdi32
kernel32 = windll.kernel32

def get_pixel(x=None, y=None):
    """Returns the pixel color of the given screen coordinate"""
    rgb = gdi.GetPixel(user32.GetDC(0), x, y)

    red = rgb & 255
    green = (rgb >> 8) & 255
    blue = (rgb >> 16) & 255
    return (red, green, blue)

