import cv2
from core.processors.base_processor import BasePoseProcessor
from core.analysis.squat_analysis import analyze_squat
from core.utils.visual_utils import draw_leg_feedback, draw_overlay_box
from core.config.thresholds import get_thresholds


class SquatProcessor(BasePoseProcessor):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.thresholds = get_thresholds(level, "squat")

    def process(self, frame, pose_model):
        if self.flip_frame:
            frame = cv2.flip(frame, 1)

        results = pose_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        feedback = {"tips": {"posture": "No person detected"}}
        left_angle = right_angle = 0

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Analyze squat
            feedback, left_angle, right_angle, left_pts, right_pts = analyze_squat(
                landmarks, frame.shape, self.thresholds
            )

            bottom_threshold = self.thresholds["KNEE_THRESH"][1]
            top_threshold = self.thresholds["KNEE_THRESH"][2]

            # Rep detection based on knee angle
            if left_angle > top_threshold and right_angle > top_threshold:
                if self.last_state == "down":
                    self.rep_count += 1
                    self.last_state = "up"
            elif left_angle < bottom_threshold and right_angle < bottom_threshold:
                if self.last_state != "down":
                    self.last_state = "down"

            frame = draw_leg_feedback(
                frame, feedback, left_pts, right_pts, left_angle, right_angle
            )

        frame = draw_overlay_box(frame, self.rep_count, feedback)
        return frame, feedback
