from core.utils.geometry_utils import calculate_angle, to_pixel


def analyze_lateral_raise(landmarks, frame_shape, thresholds):
    # Use hip–shoulder–elbow to measure lateral raise angle
    lh, ls, le = landmarks[23], landmarks[11], landmarks[13]  # Left side
    rh, rs, re = landmarks[24], landmarks[12], landmarks[14]  # Right side

    left_pts = tuple(to_pixel(pt, frame_shape) for pt in (lh, ls, le))
    right_pts = tuple(to_pixel(pt, frame_shape) for pt in (rh, rs, re))

    left_angle = calculate_angle(*left_pts)
    right_angle = calculate_angle(*right_pts)
    avg = (left_angle + right_angle) / 2

    # Extract level-specific thresholds
    min_top = thresholds["ANGLE_TOP_MIN"]
    max_top = thresholds["ANGLE_TOP_MAX"]

    tips = {}
    if avg < min_top:
        tips["posture"] = "Raise your arms higher"
    elif avg > max_top:
        tips["posture"] = "Lower your arms slightly"
    else:
        tips["posture"] = "Perfect form!"

    if abs(left_angle - right_angle) > 12:
        tips["symmetry"] = f"Uneven lift: L={int(left_angle)}°, R={int(right_angle)}°"

    feedback = {
        "tips": tips,
        "left_angle": round(left_angle, 1),
        "right_angle": round(right_angle, 1),
    }

    return feedback, left_angle, right_angle, left_pts, right_pts
