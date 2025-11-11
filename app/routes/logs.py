from fastapi import APIRouter, HTTPException
import os

router = APIRouter(prefix="/api", tags=["Logs"])

LOG_FILE = os.path.join("logs", "server.log")

@router.get("/logs/")
async def get_logs(lines: int = 50):
    """Return the last N lines from the backend log file."""
    try:
        if not os.path.exists(LOG_FILE):
            raise HTTPException(status_code=404, detail="Log file not found")

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            return {"logs": all_lines[-lines:]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
