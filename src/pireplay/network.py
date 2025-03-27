import time
from pireplay.config import Config, config

# Mock network state
cached_ssids = []


def get_ap_ssid():
    """Mock AP SSID for local development"""
    return "mock-ap"


def setup_network():
    """Mock network setup for local development"""
    pass


def refresh_cached_ssids():
    """Mock network refresh for local development"""
    cached_ssids.clear()
    cached_ssids.extend(["Mock Network 1", "Mock Network 2"])


def connected_to():
    """Mock network connection status for local development"""
    return False
