import json, pickle
import os
import shutil
import aiofiles

from game import constants
from .terrain_generation import generate_chunk


# Player
async def read_player_data():
    path = constants.PLAYER_DATA_PATH
    if not os.path.exists(path):
        # If file doesn't exist, return
        return
    async with aiofiles.open(path, "r") as rfile:
        contents = await rfile.read()
    return json.loads(contents)

async def write_player_data(data):
    contents = json.dumps(data)
    async with aiofiles.open(constants.PLAYER_DATA_PATH, "w") as wfile:
        await wfile.write(contents)
        

def clear_player_data():
    print("Clearing player data")
    if os.path.exists(constants.PLAYER_DATA_PATH):
        os.remove(constants.PLAYER_DATA_PATH)


# Read chunk from disc
async def read_chunk(chunkpos):
    path = f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}"
    if not os.path.exists(path):
        # If file doesn't exist, return None
        return

    async with aiofiles.open(path, "r") as rfile:
        contents = await rfile.read()
    return json.loads(contents)

# Write chunk to disc
async def write_chunk(chunkpos, chunk):
    if not os.path.exists(f"{constants.CHUNKS_PATH}/{chunkpos.z}/"):
        os.makedirs(f"{constants.CHUNKS_PATH}/{chunkpos.z}/")
    
    contents = json.dumps(chunk)
    async with aiofiles.open(f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}", "w") as wfile:
        await wfile.write(contents)

# For loading a chunk. Reads chunk if it exists, otherwise generates a new one
async def load_chunk(chunkpos):
    # Load chunk from disc
    c = await read_chunk(chunkpos)
    if not c:
        # Generate new chunk
        c = generate_chunk(chunkpos)
        await write_chunk(chunkpos, c)
    
    return c

# Remove all chunks
def clear_chunks():
    print("Clearing chunks")
    if os.path.exists(constants.CHUNKS_PATH):
        shutil.rmtree(constants.CHUNKS_PATH)
