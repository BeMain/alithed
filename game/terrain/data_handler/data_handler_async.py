import json, pickle
import os
import shutil
import aiofiles

from game import constants, debug
from .terrain_generation import generate_chunk


async def aread_player_data():
    """Read player data from disk asynchronously"""
    path = constants.PLAYER_DATA_PATH
    if not os.path.exists(path):
        return
    async with aiofiles.open(path, "r") as rfile:
        contents = await rfile.read()
    return json.loads(contents)

async def awrite_player_data(data):
    """Write player data to disk asynchronously"""
    contents = json.dumps(data)
    async with aiofiles.open(constants.PLAYER_DATA_PATH, "w") as wfile:
        await wfile.write(contents)


async def aread_chunk(chunkpos):
    """Read chunk from disk asynchronously"""
    path = f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}"
    if not os.path.exists(path):
        return

    async with aiofiles.open(path, "r") as rfile:
        contents = await rfile.read()
    return json.loads(contents)

async def awrite_chunk(chunkpos, chunk):
    """Write chunk to disk asynchronously"""
    # Make sure chunk directory exists
    if not os.path.exists(f"{constants.CHUNKS_PATH}/{chunkpos.z}/"):
        os.makedirs(f"{constants.CHUNKS_PATH}/{chunkpos.z}/")
    
    contents = json.dumps(chunk)
    async with aiofiles.open(f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}", "w") as wfile:
        await wfile.write(contents)

async def aload_chunk(chunkpos):
    """Reads chunk from disk asynchronously if it exists, otherwise generate a new one"""
    # Load chunk from disc
    chunk = await aread_chunk(chunkpos)
    if not chunk:
        # Generate new chunk
        chunk = generate_chunk(chunkpos)
    
    return chunk
