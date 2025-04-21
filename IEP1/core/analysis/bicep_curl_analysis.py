from core.utils.geometry_utils import calculate_angle, to_pixel


def analyze_bicep_curl(landmarks, frame_shape, thresholds):
    ls, le, lw = (
        landmarks[11],
        landmarks[13],
        landmarks[15],
    )  # Left shoulder, elbow, wrist
    rs, re, rw = (
        landmarks[12],
        landmarks[14],
        landmarks[16],
    )  # Right shoulder, elbow, wrist

    left_pts = tuple(to_pixel(pt, frame_shape) for pt in (ls, le, lw))
    right_pts = tuple(to_pixel(pt, frame_shape) for pt in (rs, re, rw))

    left_angle = calculate_angle(*left_pts)
    right_angle = calculate_angle(*right_pts)

    tips = {}
    avg_angle = (left_angle + right_angle) / 2

    min_angle = thresholds["ELBOW_MIN"]
    max_angle = thresholds["ELBOW_MAX"]

    if avg_angle > max_angle:
        tips["posture"] = "Arm fully extended"
    elif avg_angle < min_angle:
        tips["posture"] = "Full curl achieved"
    else:
        tips["posture"] = "Keep curling!"

    if abs(left_angle - right_angle) > 10:
        tips["symmetry"] = f"Asymmetry: L={int(left_angle)}°, R={int(right_angle)}°"

    feedback = {
        "tips": tips,
        "left_angle": round(left_angle, 1),
        "right_angle": round(right_angle, 1),
    }

    return feedback, left_angle, right_angle, left_pts, right_pts
