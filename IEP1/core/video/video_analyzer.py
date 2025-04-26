import cv2, os, tempfile, subprocess, importlib
import time
import uuid
from core.utils.pose_loader import get_mediapipe_pose

pose = get_mediapipe_pose()


def analyze_video_file(input_path: str, exercise: str, level: str) -> str:
    # Dynamic import of processor
    module_name = f"core.processors.{exercise}_processor"
    class_name = (
        "".join(word.capitalize() for word in exercise.split("_")) + "Processor"
    )
    try:
        module = importlib.import_module(module_name)
        processor_class = getattr(module, class_name)
        processor = processor_class(level=level)
    except (ModuleNotFoundError, AttributeError) as e:
        raise ValueError(f"Unsupported exercise: {exercise}") from e

    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

    # Temporary file paths (no permanent folder)
    raw_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    final_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    writer = cv2.VideoWriter(
        raw_out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame, _ = processor.process(frame_rgb, pose)
        writer.write(processed_frame[..., ::-1])

    cap.release()
    writer.release()

    subprocess.run(
        ["ffmpeg", "-y", "-i", raw_out, "-vcodec", "libx264", "-crf", "23", final_out],
        check=True,
    )
    os.remove(raw_out)

    return final_out
