import cv2
from core.processors.base_processor import BasePoseProcessor
from core.analysis.shoulder_press_analysis import analyze_shoulder_press
from core.utils.visual_utils import draw_arm_feedback, draw_overlay_box
from core.config.thresholds import get_thresholds


class ShoulderPressProcessor(BasePoseProcessor):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.thresholds = get_thresholds(level, "shoulder_press")

    def process(self, frame, pose_model):
        if self.flip_frame:
            frame = cv2.flip(frame, 1)

        results = pose_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        feedback = {"tips": {"posture": "No person detected"}}
        left_angle = right_angle = 0

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            feedback, left_angle, right_angle, left_pts, right_pts = (
                analyze_shoulder_press(landmarks, frame.shape, self.thresholds)
            )

            press_angle = self.thresholds["SHOULDER_PRESS_ANGLE"]
            min_depth = self.thresholds["MIN_DEPTH"]

            # Rep counting logic using thresholds
            if left_angle > press_angle and right_angle > press_angle:
                if self.last_state == "down":
                    self.rep_count += 1
                    self.last_state = "up"
            elif left_angle < min_depth and right_angle < min_depth:
                if self.last_state != "down":
                    self.last_state = "down"

            frame = draw_arm_feedback(
                frame, feedback, left_pts, right_pts, left_angle, right_angle
            )

        frame = draw_overlay_box(frame, self.rep_count, feedback)
        return frame, feedback
