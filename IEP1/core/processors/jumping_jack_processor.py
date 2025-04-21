import cv2
from core.processors.base_processor import BasePoseProcessor
from core.analysis.jumping_jack_analysis import analyze_jumping_jack
from core.utils.visual_utils import (
    draw_arm_feedback,
    draw_leg_feedback,
    draw_overlay_box,
)
from core.config.thresholds import get_thresholds


class JumpingJackProcessor(BasePoseProcessor):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.thresholds = get_thresholds(level, "jumping_jack")

    def process(self, frame, pose_model):
        if self.flip_frame:
            frame = cv2.flip(frame, 1)

        results = pose_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        feedback = {"tips": {"posture": "No person detected"}}

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            (
                feedback,
                left_arm_angle,
                right_arm_angle,
                left_leg_angle,
                right_leg_angle,
                left_arm_pts,
                right_arm_pts,
                left_leg_pts,
                right_leg_pts,
            ) = analyze_jumping_jack(landmarks, frame.shape, self.thresholds)

            # Rep logic using normalized positions
            ls = landmarks[11]  # left shoulder
            rs = landmarks[12]  # right shoulder
            lw = landmarks[15]  # left wrist
            rw = landmarks[16]  # right wrist
            la = landmarks[27]  # left ankle
            ra = landmarks[28]  # right ankle

            arm_y_thresh = self.thresholds["ARM_Y_THRESH"]
            leg_x_thresh = self.thresholds["LEG_SPREAD_X"]

            arms_up = lw.y < ls.y - arm_y_thresh and rw.y < rs.y - arm_y_thresh
            legs_apart = abs(la.x - ra.x) > leg_x_thresh
            full_open = arms_up and legs_apart

            arms_down = lw.y > ls.y + arm_y_thresh and rw.y > rs.y + arm_y_thresh
            legs_closed = abs(la.x - ra.x) < leg_x_thresh / 2
            full_closed = arms_down and legs_closed

            if full_open and self.last_state == "closed":
                self.rep_count += 1
                self.last_state = "open"
                feedback["tips"]["posture"] = "Great jump!"
            elif full_closed:
                self.last_state = "closed"
                feedback["tips"]["posture"] = "Get ready to jump!"

            frame = draw_arm_feedback(
                frame,
                feedback,
                left_arm_pts,
                right_arm_pts,
                left_arm_angle,
                right_arm_angle,
            )
            frame = draw_leg_feedback(
                frame,
                feedback,
                left_leg_pts,
                right_leg_pts,
                left_leg_angle,
                right_leg_angle,
            )

        frame = draw_overlay_box(frame, self.rep_count, feedback)
        return frame, feedback
