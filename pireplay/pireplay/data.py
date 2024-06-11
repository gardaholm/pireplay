from datetime import datetime

from pireplay.config import config, Config


def get_new_replay_name():
    return datetime.now().strftime(config(Config.replay_name))


def get_past_replays():
    # TODO get past replays from directory
    return [
        "2024_06_10 - 18:04",
        "2024_06_10 - 18:03",
        "2024_06_10 - 18:02",
        # "2024_06_10 - 18:01",
        # "2024_06_10 - 18:00",
    ]
