from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="FastAPI Hello World", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint returning a hello world message"""
    return JSONResponse(
        content={
            "message": "Hello World from FastAPI!",
            "version": "1.0.0",
            "status": "healthy"
        }
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "fastapi-hello-world"
        }
    )


@app.get("/api/v1/info")
async def info():
    """Information endpoint"""
    return JSONResponse(
        content={
            "service": "FastAPI Hello World",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

