import mediapipe as mp


def get_mediapipe_pose(static_image_mode=False, model_complexity=1):
    """
    Returns a configured Mediapipe Pose object.
    """
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=static_image_mode,
        model_complexity=model_complexity,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return pose
