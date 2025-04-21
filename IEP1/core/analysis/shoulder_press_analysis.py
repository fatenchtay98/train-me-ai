from core.utils.geometry_utils import calculate_angle, to_pixel


def analyze_shoulder_press(landmarks, frame_shape, thresholds):
    # Shoulder → Elbow → Wrist
    ls, le, lw = landmarks[11], landmarks[13], landmarks[15]
    rs, re, rw = landmarks[12], landmarks[14], landmarks[16]

    left_pts = tuple(to_pixel(pt, frame_shape) for pt in (ls, le, lw))
    right_pts = tuple(to_pixel(pt, frame_shape) for pt in (rs, re, rw))

    left_angle = calculate_angle(*left_pts)
    right_angle = calculate_angle(*right_pts)
    avg_angle = (left_angle + right_angle) / 2

    tips = {}

    press_threshold = thresholds["SHOULDER_PRESS_ANGLE"]
    min_depth = thresholds["MIN_DEPTH"]

    if avg_angle < min_depth:
        tips["posture"] = "Arms too low - push upward"
    elif avg_angle > press_threshold:
        tips["posture"] = "Arms fully extended - good!"
    else:
        tips["posture"] = "Keep pressing upward"

    if abs(left_angle - right_angle) > 12:
        tips["symmetry"] = f"Imbalance: L={int(left_angle)}°, R={int(right_angle)}°"
        if left_angle < right_angle:
            tips["correction"] = "Raise left arm more"
        else:
            tips["correction"] = "Raise right arm more"

    feedback = {
        "tips": tips,
        "left_angle": round(left_angle, 1),
        "right_angle": round(right_angle, 1),
    }

    return feedback, left_angle, right_angle, left_pts, right_pts
