def get_thresholds(level, exercise):
    is_pro = level == "pro"

    if exercise == "squat":
        return {
            "HIP_KNEE_VERT": {
                "NORMAL": (0, 32),
                "TRANS": (35, 65),
                "PASS": (80, 95) if is_pro else (70, 95),
            },
            "HIP_THRESH": [15, 50] if is_pro else [10, 50],
            "ANKLE_THRESH": 30 if is_pro else 45,
            "KNEE_THRESH": [50, 80, 95] if is_pro else [50, 70, 95],
            "OFFSET_THRESH": 35.0,
            "INACTIVE_THRESH": 15.0,
            "CNT_FRAME_THRESH": 50,
        }

    if exercise == "bicep_curl":
        return {
            "ELBOW_MIN": 45 if is_pro else 40,
            "ELBOW_MAX": 170 if is_pro else 160,
            "HOLD_FRAMES": 3,
        }

    if exercise == "shoulder_press":
        return {"SHOULDER_PRESS_ANGLE": 170 if is_pro else 160, "MIN_DEPTH": 90}

    if exercise == "jumping_jack":
        return {
            "ARM_Y_THRESH": 0.12 if is_pro else 0.15,
            "LEG_SPREAD_X": 0.30 if is_pro else 0.25,
            "ARM_ANGLE_TARGET": 160 if is_pro else 150,
            "ARM_MIN_RAISE": 90 if is_pro else 80,
            "LEG_ANGLE_TARGET": 170 if is_pro else 160,
        }

    if exercise == "tricep_extension":
        return {"ELBOW_MIN": 60 if is_pro else 70, "ELBOW_MAX": 170 if is_pro else 160}

    if exercise == "lateral_raise":
        return {
            "ANGLE_TOP_MIN": 85 if is_pro else 80,
            "ANGLE_TOP_MAX": 115 if is_pro else 110,
            "ANGLE_BOTTOM_MAX": 50 if is_pro else 60,
        }

    raise ValueError(f"Unknown exercise: {exercise}")
