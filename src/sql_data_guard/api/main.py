import logging
import os
from logging.config import fileConfig

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from sql_data_guard import verify_sql

app = FastAPI(title="SQL Data Guard REST API")


@app.post("/verify-sql")
async def verify_sql_endpoint(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Request must be JSON"},
        )

    if not isinstance(data, dict):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Request must be JSON"},
        )

    if "sql" not in data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Missing 'sql' in request"},
        )

    if "config" not in data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Missing 'config' in request"},
        )

    sql = data["sql"]
    config = data["config"]
    dialect = data.get("dialect")

    result = verify_sql(sql, config, dialect)
    result["errors"] = list(result.get("errors", []))
    return result


def _init_logging():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.conf")
    if os.path.exists(config_path):
        fileConfig(config_path)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info("Logging initialized")


_init_logging()
