import random
import colorsys

def generate_color():
    """ Generates bright colors and avoids black.
        Used to color the different EEG signal plots.
    """
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
