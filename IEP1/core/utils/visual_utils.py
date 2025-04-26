import cv2


def draw_overlay_box(frame, rep_count, feedback):
    height, width = frame.shape[:2]

    # Draw the box at the top instead of bottom
    box_height = 110
    y_start = 10
    y_end = y_start + box_height

    overlay = frame.copy()
    cv2.rectangle(overlay, (10, y_start), (width - 10, y_end), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

    # Reps count
    cv2.putText(
        frame,
        f"Reps: {rep_count}",
        (20, y_start + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
        lineType=cv2.LINE_AA,
    )

    # Posture tip
    tip = feedback.get("tips", {}).get("posture", "Good!")
    cv2.putText(
        frame,
        f"Tips: {tip}",
        (20, y_start + 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        lineType=cv2.LINE_AA,
    )

    # Optional extra tips
    tips_dict = feedback.get("tips", {})
    if len(tips_dict) > 1:
        y_offset = y_start + 90
        for k, msg in tips_dict.items():
            if k == "posture":
                continue
            cv2.putText(
                frame,
                msg,
                (20, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 255),
                2,
                lineType=cv2.LINE_AA,
            )
            y_offset += 22

    return frame


def get_angle_color(angle):
    """
    Return BGR color based on the angle value.
    """
    if angle < 90:
        return (0, 255, 0)  # Green = optimal
    elif angle > 140:
        return (0, 0, 255)  # Red = too extended
    else:
        return (0, 255, 255)  # Yellow = borderline


def draw_arm_feedback(frame, feedback, left_pts, right_pts, left_angle, right_angle):
    def draw_arm(shoulder, elbow, wrist, angle, color):
        # Draw lines
        cv2.line(frame, shoulder, elbow, color, 4, lineType=cv2.LINE_AA)
        cv2.line(frame, wrist, elbow, color, 4, lineType=cv2.LINE_AA)

        # Joints
        for pt in (shoulder, elbow, wrist):
            cv2.circle(frame, pt, 8, (255, 255, 255), -1, lineType=cv2.LINE_AA)
            cv2.circle(frame, pt, 5, color, -1, lineType=cv2.LINE_AA)

        # Angle circle + label
        angle_text = f"{int(angle)}°"
        text_size, _ = cv2.getTextSize(angle_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        text_w, text_h = text_size
        cx, cy = elbow[0], elbow[1] - 35
        cv2.circle(frame, (cx, cy), 22, color, -1, lineType=cv2.LINE_AA)
        cv2.putText(
            frame,
            angle_text,
            (cx - text_w // 2, cy + text_h // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
            lineType=cv2.LINE_AA,
        )

    # Draw both arms
    draw_arm(*left_pts, left_angle, get_angle_color(left_angle))
    draw_arm(*right_pts, right_angle, get_angle_color(right_angle))

    return frame


def draw_leg_feedback(frame, feedback, left_pts, right_pts, left_angle, right_angle):
    def draw_leg(hip, knee, ankle, angle, color, label="L"):
        # Draw anti-aliased thick lines
        cv2.line(frame, hip, knee, color, 4, lineType=cv2.LINE_AA)
        cv2.line(frame, ankle, knee, color, 4, lineType=cv2.LINE_AA)

        # Joint markers
        for pt in (hip, knee, ankle):
            cv2.circle(
                frame, pt, 8, (255, 255, 255), -1, lineType=cv2.LINE_AA
            )  # white border
            cv2.circle(frame, pt, 5, color, -1, lineType=cv2.LINE_AA)

        # Angle bubble near the knee
        angle_text = f"{int(angle)} deg"
        text_size, _ = cv2.getTextSize(angle_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        text_w, text_h = text_size
        cx, cy = knee[0], knee[1] - 35

        cv2.circle(frame, (cx, cy), 22, color, -1, lineType=cv2.LINE_AA)
        cv2.putText(
            frame,
            angle_text,
            (cx - text_w // 2 + 1, cy + text_h // 2 + 1),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            3,
            lineType=cv2.LINE_AA,
        )  # shadow
        cv2.putText(
            frame,
            angle_text,
            (cx - text_w // 2, cy + text_h // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            lineType=cv2.LINE_AA,
        )

    # Draw both legs
    draw_leg(*left_pts, left_angle, get_angle_color(left_angle), "L")
    draw_leg(*right_pts, right_angle, get_angle_color(right_angle), "R")

    return frame
