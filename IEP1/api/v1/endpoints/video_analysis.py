from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import tempfile, os

from core.video.video_analyzer import analyze_video_file

router = APIRouter()


@router.post("/analyze-video")
async def analyze_video(
    video: UploadFile = File(...), exercise: str = Form(...), level: str = Form(...)
):
    """
    Analyze uploaded video for the selected exercise (e.g., squat, bicep_curl, etc.)
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_vid:
            temp_vid.write(await video.read())
            input_path = temp_vid.name

        output_path = analyze_video_file(input_path, exercise.lower(), level.lower())
        os.remove(input_path)

        return FileResponse(
            path=output_path, media_type="video/mp4", filename=f"{exercise}_output.mp4"
        )

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
