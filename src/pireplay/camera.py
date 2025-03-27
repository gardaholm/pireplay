import os
from pireplay.config import config
from pireplay.consts import Camera, Config

# Mock camera state
_cam = None
_output = None

def setup_camera():
    """Mock camera setup for local development"""
    global _cam, _output
    _cam = None
    _output = None
    delete_snapshot()

def save_recording(path, length):
    """Mock recording save for local development"""
    # Create an empty file to simulate recording
    with open(path, "w") as file:
        file.write("")

def save_snapshot():
    """Mock snapshot save for local development"""
    # Create an empty file to simulate snapshot
    with open(Camera.SNAPSHOT_FILE, "w") as file:
        file.write("")

def delete_snapshot():
    """Delete snapshot file if it exists"""
    if os.path.isfile(Camera.SNAPSHOT_FILE):
        os.remove(Camera.SNAPSHOT_FILE)
