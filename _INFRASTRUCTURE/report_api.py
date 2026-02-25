#!/usr/bin/env python3
"""
Report API
API for accessing generated reports
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Report API")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "report-api"}

@app.get("/reports")
async def list_reports():
    return {"reports": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
