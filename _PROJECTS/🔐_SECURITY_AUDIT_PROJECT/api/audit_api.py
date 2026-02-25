#!/usr/bin/env python3
"""
Security Audit API
Main API service for security audit operations
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Security Audit API")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "audit-api"}

@app.get("/")
async def root():
    return {"message": "Security Audit API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
