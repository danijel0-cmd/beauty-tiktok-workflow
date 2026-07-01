"""Utility functions"""

import json
import logging
from pathlib import Path


def setup_logging(level=logging.INFO):
    """Setup logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def load_config(config_path: str = 'config/settings.json') -> dict:
    """Load configuration from JSON file"""
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_file, 'r') as f:
        config = json.load(f)

    return config


def save_config(config: dict, config_path: str = 'config/settings.json'):
    """Save configuration to JSON file"""
    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)


def get_timestamp_range(start: float, end: float) -> str:
    """Format timestamp range as string"""
    def format_time(seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    return f"{format_time(start)} - {format_time(end)}"
