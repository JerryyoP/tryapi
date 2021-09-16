from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from aiohttp import ClientSession
from shlex import quote
import asyncio

app = FastAPI()
session = None

async def get_session():
    global session
    if not session:
        session = ClientSession()
    return session

async def iter_stream(
    url: str,
):
    s = await get_session()
    resp = await s.get(url)
    async for data, _ in resp.content.iter_chunks():
        yield data

async def get_url(url: str):
    cmd = f"youtube-dl --get-url {quote(url)}"
    print(cmd)
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    return stdout, stderr

@app.get("/")
async def relay(url: str):
    url, err = await get_url(url)
    if url:
        url = url.decode().strip()
        return StreamingResponse(
                iter_stream(url),
                200,
                media_type="video/mp4",
        )
    elif err:
        return {"error": err}
    else:
        return {"error": "Something went wrong"}
