# Requires: fastapi uvicorn
# Install: pip install fastapi uvicorn
# Run: uvicorn app:app --reload
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI(title="Streaming Demo")

async def text_stream():
    chunks = [
        "Hello", " ", "from", " ", "a", " ", "streaming", " ", "FastAPI", " ", "endpoint", "!"
    ]
    for c in chunks:
        yield c
        await asyncio.sleep(0.2)

@app.get("/stream", response_class=StreamingResponse)
async def stream():
    return StreamingResponse(text_stream(), media_type="text/plain")

# Server-Sent Events (SSE) variant
async def sse_generator():
    for i in range(1, 6):
        yield f"data: {{\"count\": {i}}}\n\n"
        await asyncio.sleep(0.5)

@app.get("/sse")
async def sse():
    return StreamingResponse(sse_generator(), media_type="text/event-stream")
