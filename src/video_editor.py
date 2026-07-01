"""Video Editing & TikTok Optimization"""

import logging
import subprocess
from pathlib import Path
from typing import Dict
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, concatenate_videoclips

logger = logging.getLogger(__name__)


class VideoEditor:
    """Edit videos and optimize for TikTok"""

    def __init__(self, config: dict):
        self.config = config
        self.tiktok_width = config.get('tiktok', {}).get('width', 1080)
        self.tiktok_height = config.get('tiktok', {}).get('height', 1920)
        self.fps = config.get('tiktok', {}).get('fps', 30)
        self.bitrate = config.get('tiktok', {}).get('bitrate', '8M')

    def create_tiktok_video(self, input_path: str, hook: Dict, output_dir: str) -> str:
        """Create optimized TikTok video with hook as opener"""
        logger.info("Creating TikTok video with hook...")

        clip = VideoFileClip(input_path)

        # Extract hook
        hook_start = max(0, hook['start'])
        hook_end = min(clip.duration, hook['end'])
        hook_clip = clip.subclipped(hook_start, hook_end)

        # Create fast-paced opener (speed up hook)
        hook_clip = hook_clip.speedx(1.3)

        # Add rest of video at normal speed
        rest_start = hook_end
        rest_clip = clip.subclipped(rest_start, clip.duration)

        # Combine
        final = concatenate_videoclips([hook_clip, rest_clip])

        # Optimize for TikTok
        final = self._resize_for_tiktok(final)
        final = self._add_captions(final)

        output_path = Path(output_dir) / f"tiktok_{Path(input_path).stem}.mp4"
        logger.info(f"Exporting to {output_path}...")

        final.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )

        logger.info(f"✅ Exported: {output_path}")
        return str(output_path)

    def optimize_full_video(self, input_path: str, output_dir: str) -> str:
        """Optimize full video for TikTok without hook"""
        logger.info("Optimizing full video for TikTok...")

        clip = VideoFileClip(input_path)
        clip = self._resize_for_tiktok(clip)
        clip = self._add_captions(clip)

        output_path = Path(output_dir) / f"tiktok_{Path(input_path).stem}.mp4"

        clip.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )

        logger.info(f"✅ Exported: {output_path}")
        return str(output_path)

    def _resize_for_tiktok(self, clip):
        """Resize video to 9:16 aspect ratio for TikTok"""
        w, h = clip.size

        if w > h:
            # Landscape to portrait
            new_w = int(h * 9 / 16)
            x_center = w / 2
            x1 = int(x_center - new_w / 2)
            x2 = int(x_center + new_w / 2)
            clip = clip.crop(x1=x1, x2=x2)
        else:
            # Portrait adjustment if needed
            if h / w > 16 / 9:
                new_h = int(w * 16 / 9)
                y_center = h / 2
                y1 = int(y_center - new_h / 2)
                y2 = int(y_center + new_h / 2)
                clip = clip.crop(y1=y1, y2=y2)

        # Final resize to TikTok dimensions
        clip = clip.resize((self.tiktok_width, self.tiktok_height))
        return clip

    def _add_captions(self, clip, text: str = "Made with AI ✨"):
        """Add captions to video"""
        try:
            txt_clip = TextClip(
                text,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(self.tiktok_width - 100, None)
            )

            txt_clip = txt_clip.set_position('bottom').set_duration(clip.duration)
            final = CompositeVideoClip([clip, txt_clip])
            return final
        except Exception as e:
            logger.warning(f"Could not add captions: {e}")
            return clip

    def merge_multiple_clips(self, video_paths: list, output_path: str):
        """Merge multiple video clips"""
        logger.info(f"Merging {len(video_paths)} clips...")

        clips = [VideoFileClip(path) for path in video_paths]
        final = concatenate_videoclips(clips)
        final = self._resize_for_tiktok(final)

        final.write_videofile(
            output_path,
            fps=self.fps,
            codec='libx264',
            verbose=False,
            logger=None
        )

        logger.info(f"✅ Merged: {output_path}")
        return output_path

    def export_with_ffmpeg(self, input_path: str, output_path: str):
        """Alternative export using ffmpeg for better performance"""
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={self.tiktok_width}:{self.tiktok_height}:force_original_aspect_ratio=decrease,pad={self.tiktok_width}:{self.tiktok_height}:(ow-iw)/2:(oh-ih)/2',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',
            output_path
        ]

        logger.info("Exporting with ffmpeg...")
        subprocess.run(cmd, check=True)
        logger.info(f"✅ Exported: {output_path}")
        return output_path
