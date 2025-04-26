from fastapi import FastAPI
from api.v1.endpoints.video_analysis import router as video_router
from api.v1.endpoints.live_analysis import router as live_router

app = FastAPI(
    title="TrainMeAI Pose Estimation API",
    description="Analyze user poses using landmarks or uploaded video",
    version="1.0",
)

# Register landmark-based and video-based endpoints
app.include_router(video_router, prefix="/api/v1/pose")
app.include_router(live_router, prefix="/api/v1/pose")
