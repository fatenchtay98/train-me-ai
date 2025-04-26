from core.utils.geometry_utils import calculate_angle, to_pixel


def analyze_jumping_jack(landmarks, frame_shape, thresholds):
    # Arm angles (shoulder-elbow-wrist)
    ls, le, lw = landmarks[11], landmarks[13], landmarks[15]
    rs, re, rw = landmarks[12], landmarks[14], landmarks[16]

    # Leg angles (hip-knee-ankle)
    lh, lk, la = landmarks[23], landmarks[25], landmarks[27]
    rh, rk, ra = landmarks[24], landmarks[26], landmarks[28]

    # Convert to pixel points
    left_arm_pts = tuple(to_pixel(pt, frame_shape) for pt in (ls, le, lw))
    right_arm_pts = tuple(to_pixel(pt, frame_shape) for pt in (rs, re, rw))
    left_leg_pts = tuple(to_pixel(pt, frame_shape) for pt in (lh, lk, la))
    right_leg_pts = tuple(to_pixel(pt, frame_shape) for pt in (rh, rk, ra))

    # Compute angles
    left_arm_angle = calculate_angle(*left_arm_pts)
    right_arm_angle = calculate_angle(*right_arm_pts)
    left_leg_angle = calculate_angle(*left_leg_pts)
    right_leg_angle = calculate_angle(*right_leg_pts)

    tips = {}

    # Thresholds from config
    arm_target_angle = thresholds.get("ARM_ANGLE_TARGET", 150)
    arm_min_raise = thresholds.get("ARM_MIN_RAISE", 80)
    leg_spread_angle = thresholds.get("LEG_ANGLE_TARGET", 160)

    # --- Arm Tips ---
    avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
    if avg_arm_angle < arm_min_raise:
        tips["arms"] = "Raise arms higher"
    elif avg_arm_angle > arm_target_angle:
        tips["arms"] = "Arms fully extended - good!"
    else:
        tips["arms"] = "Keep pushing upward"

    # --- Leg Tips ---
    avg_leg_angle = (left_leg_angle + right_leg_angle) / 2
    if avg_leg_angle < leg_spread_angle:
        tips["legs"] = "Widen stance"
    else:
        tips["legs"] = "Good leg position"

    # --- Symmetry Tips ---
    if abs(left_arm_angle - right_arm_angle) > 10:
        tips["symmetry_arms"] = (
            f"Arm imbalance: L={int(left_arm_angle)}°, R={int(right_arm_angle)}°"
        )
    if abs(left_leg_angle - right_leg_angle) > 10:
        tips["symmetry_legs"] = (
            f"Leg imbalance: L={int(left_leg_angle)}°, R={int(right_leg_angle)}°"
        )

    feedback = {
        "tips": tips,
        "left_arm_angle": round(left_arm_angle, 1),
        "right_arm_angle": round(right_arm_angle, 1),
        "left_leg_angle": round(left_leg_angle, 1),
        "right_leg_angle": round(right_leg_angle, 1),
    }

    return (
        feedback,
        left_arm_angle,
        right_arm_angle,
        left_leg_angle,
        right_leg_angle,
        left_arm_pts,
        right_arm_pts,
        left_leg_pts,
        right_leg_pts,
    )
