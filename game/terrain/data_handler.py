import pickle, json
import os
import shutil

from game import constants
from .terrain_generation import generate_chunk


# Player
def read_player_data():
    path = constants.PLAYER_DATA_PATH
    if not os.path.exists(path):
        # If file doesn't exist, return
        return
    with open(path, "r") as readfile:
        return json.load(readfile)

def write_player_data(data):
    with open(constants.PLAYER_DATA_PATH, "w") as writefile:
        json.dump(data, writefile)

def clear_player_data():
    print("Clearing player data")
    if os.path.exists(constants.PLAYER_DATA_PATH):
        os.remove(constants.PLAYER_DATA_PATH)


# Read chunk from disc
def read_chunk(chunkpos):
    path = f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}"
    if not os.path.exists(path):
        # If file doesn't exist, return None
        return
    with open(path, "rb") as readfile:
        return pickle.load(readfile)

# Write chunk to disc
def write_chunk(chunkpos, chunk):
    if not os.path.exists(f"{constants.CHUNKS_PATH}/{chunkpos.z}/"):
        os.makedirs(f"{constants.CHUNKS_PATH}/{chunkpos.z}/")
    
    with open(f"{constants.CHUNKS_PATH}/{chunkpos.z}/{chunkpos.x}.{chunkpos.y}", "wb") as writefile:
        pickle.dump(chunk, writefile)

# For loading a chunk. Reads chunk if it exists, otherwise generates a new one
def load_chunk(chunkpos):
    # Load chunk from disc
    chunk = read_chunk(chunkpos)
    if not chunk:
        # Generate new chunk
        chunk = generate_chunk(chunkpos)
        write_chunk(chunkpos, chunk)
    
    return chunk

# Remove all chunks
def clear_chunks():
    print("Clearing chunks")
    if os.path.exists(constants.CHUNKS_PATH):
        shutil.rmtree(constants.CHUNKS_PATH)
