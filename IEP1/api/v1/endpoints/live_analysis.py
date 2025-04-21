from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import cv2
import numpy as np
import importlib
import base64
import traceback

from core.utils.pose_loader import get_mediapipe_pose

router = APIRouter()
pose = get_mediapipe_pose()


class FramePayload(BaseModel):
    session_id: str
    image: str  # base64-encoded image
    exercise: str
    level: str


session_store = {}


@router.post("/analyze-frame")
async def analyze_frame(payload: FramePayload):
    try:
        # Decode image
        img_data = base64.b64decode(payload.image)
        npimg = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Load processor per session
        module_name = f"core.processors.{payload.exercise}_processor"
        class_name = (
            "".join(word.capitalize() for word in payload.exercise.split("_"))
            + "Processor"
        )
        module = importlib.import_module(module_name)

        if payload.session_id not in session_store:
            processor_class = getattr(module, class_name)
            processor = processor_class(level=payload.level)
            session_store[payload.session_id] = processor
        else:
            processor = session_store[payload.session_id]

        # Process frame
        processed_frame, feedback = processor.process(frame, pose)

        # Encode to base64 JPEG
        _, encoded = cv2.imencode(".jpg", processed_frame)
        encoded_base64 = base64.b64encode(encoded).decode("utf-8")

        return {"frame": encoded_base64, "feedback": feedback}

    except ModuleNotFoundError:
        raise HTTPException(
            status_code=400, detail=f"Unsupported exercise: {payload.exercise}"
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
