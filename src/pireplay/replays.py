import os
import json
import time
from datetime import datetime
from pathlib import Path

from pireplay.config import Config, config
from pireplay.consts import VIDEO_EXT, Option
from pireplay.camera import save_recording


def capture_new_replay():
    replays_location = config(Config.replays_location)

    # remove latest replay if maximum number of kept replays reached
    kept_replays = [
        path for f in os.listdir(replays_location)
        if os.path.isfile(path := os.path.join(replays_location, f)) and
        f.endswith(VIDEO_EXT)
    ]
    if len(kept_replays) >= int(config(Config.kept_replays)):
        oldest_replay = min(kept_replays, key=os.path.getctime)
        os.remove(oldest_replay)

    # save new replay
    replay_name = datetime.now().strftime(config(Config.replay_name))
    replay_path = os.path.join(replays_location, replay_name + VIDEO_EXT)
    replay_length = Option.capture_times_values[int(config(Config.capture_time_index))]

    save_recording(replay_path, replay_length)

    return replay_name


def get_past_replays():
    replays_location = config(Config.replays_location)

    kept_replays = [
        f[:-len(VIDEO_EXT)]
        for f in os.listdir(replays_location)
        if os.path.isfile(os.path.join(replays_location, f)) and
        f.endswith(VIDEO_EXT)
    ]

    def replay_time(replay):
        path = os.path.join(replays_location, replay + VIDEO_EXT)
        return os.path.getctime(path)

    kept_replays.sort(key=replay_time, reverse=True)

    return kept_replays


def remove_replay(replay):
    replays_dir = get_replays_dir()
    
    # Add extension if not present
    if not replay.endswith('.mp4'):
        replay = f"{replay}.mp4"
    
    file_path = replays_dir / replay
    if not file_path.exists():
        return False

    try:
        # Remove the file
        file_path.unlink()
        
        # Remove from metadata
        metadata = load_metadata()
        if replay in metadata["replays"]:
            del metadata["replays"][replay]
            save_metadata(metadata)
        
        return True
    except Exception as e:
        return False


def remove_all_replays():
    replays_dir = config(Config.replays_location)

    if not os.path.isdir(replays_dir):
        return False

    for filename in os.listdir(replays_dir):
        if filename.endswith(VIDEO_EXT):
            file_path = os.path.join(replays_dir, filename)
            os.remove(file_path)

    return True


def get_replays_dir():
    replays_dir = Path(config(Config.replays_location))
    replays_dir.mkdir(parents=True, exist_ok=True)
    return replays_dir


def get_metadata_file():
    return get_replays_dir() / "replay_metadata.json"


def load_metadata():
    metadata_file = get_metadata_file()
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            return json.load(f)
    return {"replays": {}}


def save_metadata(metadata):
    metadata_file = get_metadata_file()
    # Ensure the directory exists
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)
        # Verify the file was created and has content
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                content = f.read()
                return True
        return False
    except Exception as e:
        return False


def get_replay_name(filename):
    
    # Add extension if not present
    if not filename.endswith('.mp4'):
        filename = f"{filename}.mp4"
    
    metadata = load_metadata()
    
    if filename in metadata["replays"]:
        name = metadata["replays"][filename].get("name", "")
        return name
    else:
        return ""


def set_replay_name(filename, name):
    """Set a custom name for a replay."""
    metadata = load_metadata()
    if filename not in metadata["replays"]:
        metadata["replays"][filename] = {}
    metadata["replays"][filename]["name"] = name
    save_metadata(metadata)


def get_replays():
    """Get a list of replay files."""
    replays_dir = get_replays_dir()
    return sorted(
        [f.name for f in replays_dir.glob("*.mp4")],
        reverse=True,
    )


def delete_replay(filename):
    replays_dir = get_replays_dir()
    file_path = replays_dir / filename
    if file_path.exists():
        file_path.unlink()
        # Also remove from metadata
        metadata = load_metadata()
        if filename in metadata["replays"]:
            del metadata["replays"][filename]
            save_metadata(metadata)


def delete_all_replays():
    replays_dir = get_replays_dir()
    for file_path in replays_dir.glob("*.mp4"):
        file_path.unlink()
    # Clear metadata
    save_metadata({"replays": {}})


def rename_replay(old_name, new_name):
    replays_dir = get_replays_dir()
    
    # Ensure the replays directory exists
    replays_dir.mkdir(parents=True, exist_ok=True)
    
    # Add extension if not present
    if not old_name.endswith('.mp4'):
        old_name = f"{old_name}.mp4"
    
    file_path = replays_dir / old_name
    if not file_path.exists():
        return False
    
    try:
        metadata = load_metadata()
        if old_name not in metadata["replays"]:
            metadata["replays"][old_name] = {}
        metadata["replays"][old_name]["name"] = new_name
        
        if not save_metadata(metadata):
            return False
            
        return True
    except Exception as e:
        return False
