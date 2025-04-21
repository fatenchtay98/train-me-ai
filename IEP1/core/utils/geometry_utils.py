import numpy as np


def calculate_angle(a, b, c):
    """
    Calculate the angle between three points (a, b, c) in degrees.
    Points should be (x, y) pixel tuples.
    """
    a, b, c = np.array(a), np.array(b), np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

    return round(np.degrees(angle), 2)


def to_pixel(landmark, image_shape):
    """
    Converts a normalized landmark (x: 0–1, y: 0–1) to pixel coordinates.
    """
    h, w = image_shape[:2]
    return int(landmark.x * w), int(landmark.y * h)
