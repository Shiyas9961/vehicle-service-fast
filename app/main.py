import logging
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.logging_config import configure_logging
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleResponse

log_file = configure_logging()
app_logger = logging.getLogger("app")
request_logger = logging.getLogger("app.requests")


@asynccontextmanager
async def lifespan(_: FastAPI):
    app_logger.info("Vehicle service started. Logs are available on stdout and in %s", log_file.resolve())
    yield


app = FastAPI(title="Vehicle Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/api/metrics", include_in_schema=False)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started_at = perf_counter()
    client_host = request.client.host if request.client else "-"
    path = request.url.path
    if request.url.query:
        path = f"{path}?{request.url.query}"

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        request_logger.error(
            'client=%s method=%s path="%s" status=500 duration_ms=%.2f',
            client_host,
            request.method,
            path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    log_method = request_logger.error if response.status_code >= 500 else request_logger.info
    log_method(
        'client=%s method=%s path="%s" status=%s duration_ms=%.2f',
        client_host,
        request.method,
        path,
        response.status_code,
        duration_ms,
    )

    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/vehicles", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@app.get("/api/vehicles", response_model=list[VehicleResponse])
def list_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()
