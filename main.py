from fastapi import FastAPI, status, HTTPException, BackgroundTasks, Depends
from fastapi.responses import RedirectResponse

from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session

from fetcher import fetch_page, FetchError
from analyzer import analyze_page
from db import engine, Check

app = FastAPI(title="PageCheck", version="0.1.0")


@app.get("/", include_in_schema=False)
def root():
    """Redirect root / to /docs"""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    """Check API status return it as ok."""
    return {"status": "ok"}


class CheckRequest(BaseModel):
    url: HttpUrl


class CheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    status: str
    url: str
    created_at: datetime
    result: dict | None = None
    error: str | None = None


def get_session():
    with Session(engine) as session:
        yield session


@app.post(
    "/checks",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CheckOut,
    response_model_exclude_none=True,
)
def create_check(
    request: CheckRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """Create a check job and return it as queued."""
    url = request.url
    check_id = str(uuid4())
    session.add(
        Check(id=check_id, status="queued", url=str(url), created_at=datetime.now())
    )
    session.commit()
    background_tasks.add_task(run_check, check_id, str(url))
    check = session.get(Check, check_id)
    return check


@app.get(
    "/checks/{check_id}", response_model=CheckOut, response_model_exclude_none=True
)
def get_check(check_id: str, session: Session = Depends(get_session)):
    """Return check if id exists, or return 404 if id is not found"""
    check = session.get(Check, check_id)
    if check is None:
        raise HTTPException(status_code=404, detail="ID not found")
    return check


def run_check(check_id: str, url: str) -> None:
    """Run a check to fetch page change status to done or failed"""
    with Session(engine) as session:
        check = session.get(Check, check_id)
        try:
            html = fetch_page(url)
            check.result = analyze_page(html)
            check.status = "done"
            session.commit()
        except FetchError as e:
            check.status = "failed"
            check.error = str(e)
            session.commit()
        except Exception as e:
            check.status = "failed"
            check.error = str(e)
            session.commit()
