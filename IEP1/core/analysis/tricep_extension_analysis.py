from core.utils.geometry_utils import to_pixel, calculate_angle


def analyze_tricep_extension(landmarks, frame_shape, thresholds):
    # Get 3D normalized landmarks
    ls, le, lw = landmarks[11], landmarks[13], landmarks[15]  # Left arm
    rs, re, rw = landmarks[12], landmarks[14], landmarks[16]  # Right arm

    # Convert to 2D pixel coordinates
    left_pts = tuple(to_pixel(pt, frame_shape) for pt in (ls, le, lw))
    right_pts = tuple(to_pixel(pt, frame_shape) for pt in (rs, re, rw))

    # Elbow angle: Shoulder - Elbow - Wrist
    left_angle = calculate_angle(*left_pts)
    right_angle = calculate_angle(*right_pts)
    avg_angle = (left_angle + right_angle) / 2

    # Thresholds from config
    min_angle = thresholds["ELBOW_MIN"]
    max_angle = thresholds["ELBOW_MAX"]

    tips = {}

    if avg_angle < min_angle:
        tips["posture"] = "Extend your arms more (straighten elbows)"
    elif avg_angle > max_angle:
        tips["posture"] = "Good full extension!"
    else:
        tips["posture"] = "Almost there! Extend a bit more."

    if abs(left_angle - right_angle) > 12:
        tips["symmetry"] = (
            f"Uneven extension: L={int(left_angle)}°, R={int(right_angle)}°"
        )

    feedback = {
        "tips": tips,
        "left_angle": round(left_angle, 1),
        "right_angle": round(right_angle, 1),
    }

    return feedback, left_angle, right_angle, left_pts, right_pts
