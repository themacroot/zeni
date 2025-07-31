from fastapi import FastAPI, Request
import logging

def setup_middlewares(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logging.info(f"{request.method} {request.url}")
        response = await call_next(request)
        logging.info(f"Completed with {response.status_code}")
        return response
