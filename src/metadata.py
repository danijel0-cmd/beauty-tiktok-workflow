"""Metadata Generation for TikTok Videos"""

import logging
import json
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


class MetadataGenerator:
    """Generate captions, hashtags, and descriptions for videos"""

    BEAUTY_KEYWORDS = [
        'makeup', 'skincare', 'beauty', 'tutorial', 'transformation',
        'tips', 'routine', 'glow', 'natural', 'trends', 'viral',
        'before-after', 'glowup', 'makeup-artist', 'cosmetics'
    ]

    VIRAL_EMOJIS = ['✨', '💄', '✨', '🌟', '💅', '🎀', '💋', '👄', '💅', '🧴']

    TRENDING_HASHTAGS = [
        '#BeautyTok', '#MakeupTutorial', '#SkincareRoutine', '#BeautyTips',
        '#MakeupArtist', '#BeautyChannel', '#Transformation', '#BeforeAfter',
        '#Viral', '#FYP', '#ForYou', '#BeautyHack', '#MakeupHack',
        '#GirlsWhoCode', '#BeautyTrend'
    ]

    def __init__(self, config: dict):
        self.config = config
        self.include_emojis = config.get('metadata', {}).get('include_emojis', True)
        self.auto_hashtags = config.get('metadata', {}).get('auto_hashtags', True)

    def generate(self, input_path: str, output_path: str) -> Dict:
        """Generate complete metadata for a video"""
        logger.info("Generating metadata...")

        filename = Path(output_path).stem
        duration = self._get_video_duration(output_path)

        metadata = {
            'title': self._generate_title(filename, duration),
            'description': self._generate_description(filename),
            'hashtags': self._generate_hashtags() if self.auto_hashtags else [],
            'duration': duration,
            'format': 'tiktok',
            'optimization': {
                'hook': True,
                'aspect_ratio': '9:16',
                'duration_optimized': duration < 60,
            }
        }

        logger.info(f"Generated metadata: {json.dumps(metadata, indent=2)}")
        return metadata

    def _generate_title(self, filename: str, duration: float) -> str:
        """Generate engaging title"""
        titles = [
            f"✨ {filename} - Don't scroll! 🌟",
            f"💄 You need to see this! {filename}",
            f"🎀 {filename} - Beauty hack",
            f"🌟 The transformation you didn't expect... {filename}",
            f"💅 Watch till the end! {filename}"
        ]
        return titles[hash(filename) % len(titles)]

    def _generate_description(self, filename: str) -> str:
        """Generate description with call-to-action"""
        descriptions = [
            "💬 Comment your favorite step!\n❤️ Like if you'd try this\n👉 Follow for more beauty hacks",
            "✨ Save this for later!\n📍 Tag someone you'd share this with\n🔔 Turn on notifications for more",
            "👀 How many of you knew this trick?\n💯 This changed my routine\n✌️ Drop a comment below!",
            "🌟 This is a game changer!\n💫 Full tutorial on my page\n⬇️ DM me if you want the details"
        ]
        return descriptions[hash(filename) % len(descriptions)]

    def _generate_hashtags(self) -> list:
        """Generate trending hashtags"""
        import random
        hashtags = random.sample(self.TRENDING_HASHTAGS, min(10, len(self.TRENDING_HASHTAGS)))

        if self.include_emojis:
            hashtags = [f"{tag} {random.choice(self.VIRAL_EMOJIS)}" for tag in hashtags]

        return hashtags

    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds"""
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.close()
            return duration
        except Exception as e:
            logger.warning(f"Could not determine duration: {e}")
            return 0.0

    def export_metadata(self, metadata: Dict, output_path: str):
        """Export metadata to JSON file"""
        json_path = Path(output_path).with_suffix('.json')

        with open(json_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Metadata exported to {json_path}")
        return str(json_path)

    def create_caption_file(self, metadata: Dict, output_path: str) -> str:
        """Create a caption file for TikTok"""
        caption_path = Path(output_path).with_suffix('.txt')

        caption = f"""{metadata['title']}

{metadata['description']}

{' '.join(metadata['hashtags'])}
"""

        with open(caption_path, 'w') as f:
            f.write(caption)

        logger.info(f"Caption exported to {caption_path}")
        return str(caption_path)
