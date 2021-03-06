import math
from typing import List, Optional

import numpy as np
from PIL import Image, ImageDraw


def create_tsp_art(nodes, solution_tour: List[int], size, im_arr: Optional[any] = None,
                   darkness: bool = False) -> Image:
    im = Image.new('L', size, 255 * (1 - darkness))
    draw = ImageDraw.Draw(im)
    circle = np.array(solution_tour)
    np.append(circle, solution_tour[0])
    for i, node in enumerate(circle[:-1]):
        node1 = nodes[node]
        node2 = nodes[circle[i + 1]]
        thickness = 0
        line_fill = 255 * darkness
        if im_arr is not None:
            thickness = get_line_thickness(im_arr, node1, node2, im_arr.shape, darkness)
        draw.line((node1[0], node1[1], node2[0], node2[1]), fill=line_fill, width=thickness)
    return im


def get_line_thickness(im_arr, node1, node2, shape, darkness: bool = False) -> int:
    pixels_between_line = [pixel for pixel in interpolate_pixels_along_line(node1[1], node1[0], node2[1], node2[0]) if
                           pixel[0] < shape[0] and pixel[1] < shape[1]]
    values = [im_arr[pixel] for pixel in pixels_between_line]
    av_brightness: float = sum(values) / (255. * len(values))
    if not darkness:
        av_brightness = 1. - av_brightness
    return round(2 * av_brightness + 1)


def interpolate_pixels_along_line(x0, y0, x1, y1):
    """Uses Xiaolin Wu's line algorithm to interpolate all of the pixels along a
    straight line, given two points (x0, y0) and (x1, y1)

    Wikipedia article containing pseudo code that function was based off of:
        http://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm

    Source of code: https://stackoverflow.com/questions/24702868/python3-pillow-get-all-pixels-on-a-line
    """
    pixels = []
    steep = abs(y1 - y0) > abs(x1 - x0)

    # Ensure that the path to be interpolated is shallow and from left to right
    if steep:
        t = x0
        x0 = y0
        y0 = t

        t = x1
        x1 = y1
        y1 = t

    if x0 > x1:
        t = x0
        x0 = x1
        x1 = t

        t = y0
        y0 = y1
        y1 = t

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx  # slope

    # Get the first given coordinate and add it to the return list
    x_end = round(x0)
    y_end = y0 + (gradient * (x_end - x0))
    xpxl0 = x_end
    ypxl0 = round(y_end)
    if steep:
        pixels.extend([(ypxl0, xpxl0), (ypxl0 + 1, xpxl0)])
    else:
        pixels.extend([(xpxl0, ypxl0), (xpxl0, ypxl0 + 1)])

    interpolated_y = y_end + gradient

    # Get the second given coordinate to give the main loop a range
    x_end = round(x1)
    y_end = y1 + (gradient * (x_end - x1))
    xpxl1 = x_end
    ypxl1 = round(y_end)

    # Loop between the first x coordinate and the second x coordinate, interpolating the y coordinates
    for x in range(xpxl0 + 1, xpxl1):
        if steep:
            pixels.extend([(math.floor(interpolated_y), x), (math.floor(interpolated_y) + 1, x)])

        else:
            pixels.extend([(x, math.floor(interpolated_y)), (x, math.floor(interpolated_y) + 1)])

        interpolated_y += gradient

    # Add the second given coordinate to the given list
    if steep:
        pixels.extend([(ypxl1, xpxl1), (ypxl1 + 1, xpxl1)])
    else:
        pixels.extend([(xpxl1, ypxl1), (xpxl1, ypxl1 + 1)])

    return pixels
