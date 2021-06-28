import json, pickle
import os
import shutil
import aiofiles

from game import constants, debug
from .terrain_generation import generate_chunk


async def read_player_data():
    path = constants.PLAYER_DATA_PATH
    if not os.path.exists(path):
        return
    async with aiofiles.open(path, "r") as rfile:
        contents = await rfile.read()
    return json.loads(contents)

async def write_player_data(data):
    contents = json.dumps(data)
    async with aiofiles.open(constants.PLAYER_DATA_PATH, "w") as wfile:
        await wfile.write(contents)
        

def clear_player_data():
    debug.log("Clearing player data", priority=2)
    if os.path.exists(constants.PLAYER_DATA_PATH):
        os.remove(constants.PLAYER_DATA_PATH)


async def read_chunk(chunkpos):
    """Read chunk from disk"""
    path = f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}"
    if not os.path.exists(path):
        return

    async with aiofiles.open(path, "r") as rfile:
        contents = await rfile.read()
    return json.loads(contents)

async def write_chunk(chunkpos, chunk):
    """Write chunk to disk"""
    # Make sure chunk directory exists
    if not os.path.exists(f"{constants.CHUNKS_PATH}/{chunkpos.z}/"):
        os.makedirs(f"{constants.CHUNKS_PATH}/{chunkpos.z}/")
    
    contents = json.dumps(chunk)
    async with aiofiles.open(f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}", "w") as wfile:
        await wfile.write(contents)

async def load_chunk(chunkpos):
    """Reads chunk from disk if it exists, otherwise generate a new one"""
    # Load chunk from disc
    chunk = await read_chunk(chunkpos)
    if not chunk:
        # Generate new chunk
        chunk = generate_chunk(chunkpos)
    
    return chunk

def clear_chunks():
    """Remove all chunks from disk"""
    debug.log("Clearing chunks", priority=2)
    if os.path.exists(constants.CHUNKS_PATH):
        shutil.rmtree(constants.CHUNKS_PATH)
