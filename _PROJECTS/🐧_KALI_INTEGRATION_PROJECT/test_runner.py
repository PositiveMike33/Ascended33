#!/usr/bin/env python3
"""
Kali Labs Test Runner
Health check service for Docker container
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Kali Labs Test Runner")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "kali-labs"}

@app.get("/")
async def root():
    return {"message": "Kali Labs Test Runner"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
