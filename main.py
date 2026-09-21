from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import uuid4

app = FastAPI(title="PageCheck", version="0.1.0")
checks = {}


@app.get("/health")
def health_check():
    """Check API status return it as ok."""
    return {"status": "ok"}


class CheckRequest(BaseModel):
    url: HttpUrl


@app.post("/checks", status_code=status.HTTP_202_ACCEPTED)
def create_check(request: CheckRequest):
    """Create a check job and return it as queued."""
    url = request.url
    check_id = str(uuid4())
    checks[check_id] = {
        "id": check_id,
        "status": "queued",
        "url": url,
        "created_at": datetime.now(),
    }
    return checks[check_id]


@app.get("/checks/{check_id}")
def get_check(check_id: str):
    """Return check if id exists, or return 404 if id is not found"""
    if check_id not in checks:
        raise HTTPException(status_code=404, detail="ID not found")
    return checks[check_id]
