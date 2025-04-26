import cv2
from core.processors.base_processor import BasePoseProcessor
from core.analysis.tricep_extension_analysis import analyze_tricep_extension
from core.utils.visual_utils import draw_arm_feedback, draw_overlay_box
from core.config.thresholds import get_thresholds


class TricepExtensionProcessor(BasePoseProcessor):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.thresholds = get_thresholds(level, "tricep_extension")

    def process(self, frame, pose_model):
        if self.flip_frame:
            frame = cv2.flip(frame, 1)

        results = pose_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        feedback = {"tips": {"posture": "No person detected"}}
        left_angle = right_angle = 0

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            feedback, left_angle, right_angle, left_pts, right_pts = (
                analyze_tricep_extension(landmarks, frame.shape, self.thresholds)
            )

            min_angle = self.thresholds["ELBOW_MIN"]
            max_angle = self.thresholds["ELBOW_MAX"]

            # Rep counting logic based on elbow extension
            if left_angle < min_angle and right_angle < min_angle:
                if self.last_state != "down":
                    self.last_state = "down"
            elif left_angle > max_angle and right_angle > max_angle:
                if self.last_state == "down":
                    self.rep_count += 1
                    self.last_state = "up"

            frame = draw_arm_feedback(
                frame, feedback, left_pts, right_pts, left_angle, right_angle
            )

        frame = draw_overlay_box(frame, self.rep_count, feedback)
        return frame, feedback
