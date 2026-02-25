#!/usr/bin/env python3
"""
Webhook Handler
Handles webhook events from Pieces OS
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Webhook Handler")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "webhook-handler"}

@app.post("/webhook")
async def handle_webhook(data: dict):
    return {"status": "received", "message": "Webhook processed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
