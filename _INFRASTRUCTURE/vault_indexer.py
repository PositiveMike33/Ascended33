#!/usr/bin/env python3
"""
Vault Indexer
Indexes vault content for search capabilities
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Vault Indexer")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "vault-indexer"}

@app.get("/")
async def root():
    return {"message": "Vault Indexer"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
