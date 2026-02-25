#!/usr/bin/env python3
"""
Pieces Sync Service
Synchronization service for Pieces OS integration
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Pieces Sync")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pieces-sync"}

@app.get("/")
async def root():
    return {"message": "Pieces Sync Service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
