#!/usr/bin/env python3
"""
Crawler
Crawls vault content for indexing
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Crawler")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "crawler"}

@app.post("/crawl")
async def start_crawl():
    return {"status": "crawl_started", "message": "Crawling initiated"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
