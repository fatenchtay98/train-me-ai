from core.utils.geometry_utils import calculate_angle, to_pixel


def analyze_squat(landmarks, frame_shape, thresholds):
    lh, lk, la = landmarks[23], landmarks[25], landmarks[27]
    rh, rk, ra = landmarks[24], landmarks[26], landmarks[28]

    # Convert to pixel coordinates
    left_pts = tuple(to_pixel(pt, frame_shape) for pt in (lh, lk, la))
    right_pts = tuple(to_pixel(pt, frame_shape) for pt in (rh, rk, ra))

    # Calculate angles
    left_angle = calculate_angle(*left_pts)
    right_angle = calculate_angle(*right_pts)
    avg_angle = (left_angle + right_angle) / 2

    tips = {}

    # Thresholds
    low_thresh = thresholds["KNEE_THRESH"][0]
    good_range_start = thresholds["KNEE_THRESH"][1]
    good_range_end = thresholds["KNEE_THRESH"][2]
    high_thresh = 140

    # --- Advanced Posture Feedback ---
    if left_angle < low_thresh or right_angle < low_thresh:
        tips["posture"] = "Too deep, rise slightly"
    elif left_angle > high_thresh and right_angle > high_thresh:
        tips["posture"] = "Go lower for full squat"
    elif good_range_start <= avg_angle <= good_range_end:
        tips["posture"] = "Great squat depth"
    else:
        tips["posture"] = "Almost there! Keep form steady"

    # --- Leg Symmetry ---
    if abs(left_angle - right_angle) > 10:
        tips["symmetry"] = (
            f"Asymmetry detected: L={int(left_angle)}°, R={int(right_angle)}°"
        )
        if left_angle < right_angle:
            tips["correction"] = "Shift weight to left leg"
        else:
            tips["correction"] = "Shift weight to right leg"

    feedback = {
        "tips": tips,
        "left_angle": round(left_angle, 1),
        "right_angle": round(right_angle, 1),
    }

    return feedback, left_angle, right_angle, left_pts, right_pts
