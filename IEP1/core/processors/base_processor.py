import cv2


class BasePoseProcessor:
    def __init__(self, thresholds=None, flip_frame=True):
        self.thresholds = thresholds or {}
        self.flip_frame = flip_frame
        self.rep_count = 0
        self.last_state = None

    def process(self, frame, pose_model):
        raise NotImplementedError("Subclasses must implement this method.")

    def reset(self):
        self.rep_count = 0
        self.last_state = None

    def draw_feedback(self, frame, feedback_text):
        # Determine color based on feedback
        if "good" in feedback_text.lower():
            color = (0, 255, 0)  # Green
        elif "try" in feedback_text.lower() or "lower" in feedback_text.lower():
            color = (0, 0, 255)  # Red
        else:
            color = (255, 255, 0)  # Yellow/Neutral

        # Draw semi-transparent banner
        overlay = frame.copy()
        banner_height = 90
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], banner_height), (0, 0, 0), -1)
        alpha = 0.5
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        # Draw feedback and rep count with outline
        def draw_text(text, pos, color):
            x, y = pos
            cv2.putText(
                frame,
                text,
                (x, y),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0,
                (0, 0, 0),
                4,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1.0, color, 2, cv2.LINE_AA
            )

        draw_text(f"{feedback_text}", (20, 50), color)
        draw_text(f"Reps: {self.rep_count}", (20, 85), (255, 255, 255))

        return frame
