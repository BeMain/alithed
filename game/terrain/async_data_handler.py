import pickle
import json
import os
import shutil
from aiofile import async_open

from game import constants, debug
from .terrain_generation import generate_chunk


async def read_player_data():
    path = constants.PLAYER_DATA_PATH
    if not os.path.exists(path):
        return
    async with async_open(path, "r") as f:
        data = await f.read()
    return json.loads(readfile)


async def write_player_data(data):
    async with async_open(constants.PLAYER_DATA_PATH, "w") as f:
        await f.write(json.dumps(data))


def clear_player_data():
    debug.log("Clearing player data", priority=2)
    if os.path.exists(constants.PLAYER_DATA_PATH):
        os.remove(constants.PLAYER_DATA_PATH)


async def read_chunk(chunkpos):
    """Read chunk from disk"""
    path = f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}"
    if not os.path.exists(path):
        return
    async with async_open(path, "rb") as f:
        data = await f.read()
    return pickle.loads(data)


async def write_chunk(chunkpos, chunk):
    """Write chunk to disk"""
    # Make sure chunk directory exists
    if not os.path.exists(f"{constants.CHUNKS_PATH}/{chunkpos.z}/"):
        os.makedirs(f"{constants.CHUNKS_PATH}/{chunkpos.z}/")

    data = pickle.dumps(data)
    async with async_open(f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}", "wb") as f:
        await f.write(data)


async def load_chunk(chunkpos):
    """Reads chunk from disk if it exists, otherwise generate a new one"""
    chunk = await read_chunk(chunkpos)
    if not chunk:
        chunk = generate_chunk(chunkpos)

    return chunk


def clear_chunks():
    """Remove all chunks from disk"""
    debug.log("Clearing chunks", priority=2)
    if os.path.exists(constants.CHUNKS_PATH):
        shutil.rmtree(constants.CHUNKS_PATH)
