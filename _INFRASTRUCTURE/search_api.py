#!/usr/bin/env python3
"""
Search API
API for searching indexed vault content
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Search API")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "search-api"}

@app.get("/search")
async def search(q: str = ""):
    return {"query": q, "results": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
