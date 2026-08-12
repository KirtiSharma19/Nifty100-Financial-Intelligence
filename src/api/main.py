import time
import logging
import math
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.utils.database import get_connection
from src.api.routers.companies import router as companies_router
from src.api.routers.screener import router as screener_router
from src.api.routers.sectors import router as sectors_router
from src.api.routers.peers import router as peers_router
from src.api.routers.valuation import router as valuation_router
from src.api.routers.portfolio import router as portfolio_router
from src.api.routers.documents import router as documents_router

# --------------------------------------------------
# Application start time
# --------------------------------------------------

START_TIME = time.time()


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------
class SafeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        def sanitize(value):
            if isinstance(value, dict):
                return {
                    key: sanitize(val)
                    for key, val in value.items()
                }

            if isinstance(value, list):
                return [sanitize(item) for item in value]

            if isinstance(value, float):
                if not math.isfinite(value):
                    return None

            return value

        return super().render(sanitize(content))
    
app = FastAPI(
    title="NIFTY100 Financial Intelligence API",
    version="1.0.0",
    description="REST API for NIFTY100 financial analysis and screening",
    default_response_class=SafeJSONResponse,
)
# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    companies_router,
    prefix="/api/v1"
)
app.include_router(
    screener_router,
    prefix="/api/v1"
)
app.include_router(
    sectors_router,
    prefix="/api/v1"
)
app.include_router(
    peers_router,
    prefix="/api/v1"
)
app.include_router(
    valuation_router,
    prefix="/api/v1"
)
app.include_router(
    portfolio_router,
    prefix="/api/v1"
)
app.include_router(
    documents_router,
    prefix="/api/v1"
)

# --------------------------------------------------
# Request Logging Middleware
# --------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    response_time = (time.time() - start_time) * 1000

    logger.info(
        "%s %s | status=%s | response_time=%.2fms",
        request.method,
        request.url.path,
        response.status_code,
        response_time,
    )

    return response


# --------------------------------------------------
# Health Endpoint
# --------------------------------------------------

@app.get("/api/v1/health")
def health():
    """
    Return API health status, database row counts,
    uptime and API version.
    """

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Get all user-created tables
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )

        tables = [row[0] for row in cursor.fetchall()]

        # Count rows in every table
        db_row_counts = {}

        for table in tables:
            safe_table_name = table.replace('"', '""')

            cursor.execute(
                f'SELECT COUNT(*) FROM "{safe_table_name}"'
            )

            db_row_counts[table] = cursor.fetchone()[0]

    finally:
        conn.close()

    uptime_seconds = round(time.time() - START_TIME, 2)

    return {
        "status": "ok",
        "db_row_counts": db_row_counts,
        "uptime_seconds": uptime_seconds,
        "version": "1.0.0",
    }