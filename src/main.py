#!/usr/bin/env python3
"""Beauty TikTok Auto-Workflow - Main Entry Point"""

import os
import sys
import json
import click
import logging
from pathlib import Path
from dotenv import load_dotenv

from google_drive import GoogleDriveManager
from hook_detector import HookDetector
from video_editor import VideoEditor
from metadata import MetadataGenerator
from utils import setup_logging, load_config

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)


class BeautyTikTokWorkflow:
    def __init__(self):
        self.config = load_config()
        self.drive_manager = GoogleDriveManager()
        self.hook_detector = HookDetector(self.config)
        self.video_editor = VideoEditor(self.config)
        self.metadata_gen = MetadataGenerator(self.config)

    def process_video(self, input_path: str, output_dir: str = None) -> dict:
        """Process a single video end-to-end."""
        if output_dir is None:
            output_dir = "data/processed"

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        logger.info(f"Processing video: {input_path}")

        # Step 1: Detect hooks
        logger.info("🎯 Detecting hooks...")
        hooks = self.hook_detector.detect_hooks(input_path)
        logger.info(f"Found {len(hooks)} potential hooks")

        # Step 2: Edit video with best hook
        logger.info("✂️ Editing video...")
        if hooks:
            best_hook = hooks[0]  # Most confident hook
            output_video = self.video_editor.create_tiktok_video(
                input_path, best_hook, output_dir
            )
        else:
            logger.warning("No hooks detected, using full video")
            output_video = self.video_editor.optimize_full_video(input_path, output_dir)

        # Step 3: Generate metadata
        logger.info("📊 Generating metadata...")
        metadata = self.metadata_gen.generate(input_path, output_video)

        logger.info(f"✅ Video processed: {output_video}")
        return {
            "video": output_video,
            "hooks": hooks,
            "metadata": metadata
        }

    def process_from_drive(self, folder_id: str = None) -> list:
        """Process all videos from Google Drive folder."""
        if folder_id is None:
            folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

        logger.info(f"Fetching videos from Google Drive folder: {folder_id}")

        videos = self.drive_manager.list_videos(folder_id)
        logger.info(f"Found {len(videos)} videos")

        results = []
        for video_file in videos:
            try:
                local_path = self.drive_manager.download_file(
                    video_file['id'],
                    video_file['name']
                )
                result = self.process_video(local_path)

                # Upload result back to Drive
                self.drive_manager.upload_file(
                    result['video'],
                    folder_id,
                    f"[DONE] {Path(local_path).stem}.mp4"
                )

                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {video_file['name']}: {e}")

        return results


@click.group()
def cli():
    """Beauty TikTok Auto-Workflow CLI"""
    pass


@cli.command()
@click.option('--input', '-i', required=True, help='Input video path')
@click.option('--output', '-o', default='data/processed', help='Output directory')
def process(input, output):
    """Process a single video."""
    workflow = BeautyTikTokWorkflow()
    result = workflow.process_video(input, output)
    click.echo(json.dumps(result, indent=2, default=str))


@cli.command()
@click.option('--folder-id', '-f', help='Google Drive folder ID (or use .env)')
def sync(folder_id):
    """Sync and process all videos from Google Drive."""
    workflow = BeautyTikTokWorkflow()
    results = workflow.process_from_drive(folder_id)
    click.echo(f"✅ Processed {len(results)} videos")


@cli.command()
def setup():
    """Interactive setup wizard."""
    click.echo("🎬 Beauty TikTok Workflow Setup")
    click.echo("=" * 50)

    # Check Google Drive credentials
    creds_path = "config/google-credentials.json"
    if not Path(creds_path).exists():
        click.echo("\n⚠️  Google Drive credentials not found!")
        click.echo("1. Go to: https://console.cloud.google.com")
        click.echo("2. Create a new project")
        click.echo("3. Enable Google Drive API")
        click.echo("4. Create a service account & download JSON")
        click.echo(f"5. Save it to: {creds_path}")
    else:
        click.echo("✅ Google Drive credentials found")

    # Test connection
    if Path(creds_path).exists():
        try:
            workflow = BeautyTikTokWorkflow()
            click.echo("✅ Google Drive connection successful!")
        except Exception as e:
            click.echo(f"❌ Google Drive connection failed: {e}")

    click.echo("\n✅ Setup complete! Run 'python main.py sync' to start processing")


if __name__ == '__main__':
    cli()
