#!/usr/bin/env python3
"""
Beauty TikTok Shorts + Google Drive Integration
Automatisch Videos von Drive abrufen → Verarbeiten → Zurück speichern
"""

import cv2
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    HAS_GOOGLE_DRIVE = True
except ImportError:
    HAS_GOOGLE_DRIVE = False
    print("⚠️  Google Drive API nicht installiert. Using local files only.")

class BeautyTikTokShortsWithDrive:
    """Production workflow with Google Drive integration"""

    def __init__(self):
        self.config = {
            'tiktok_width': 1080,
            'tiktok_height': 1920,
            'fps': 30,
        }

        self.local_raw = Path('data/raw')
        self.local_output = Path('data/processed')
        self.local_raw.mkdir(parents=True, exist_ok=True)
        self.local_output.mkdir(parents=True, exist_ok=True)

        self.drive_service = None
        self.raw_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

        if HAS_GOOGLE_DRIVE and self.raw_folder_id:
            self._init_drive()

    def _init_drive(self):
        """Initialize Google Drive connection"""
        try:
            creds_path = 'config/google-credentials.json'
            if not Path(creds_path).exists():
                print("⚠️  Credentials nicht gefunden. Using local mode only.")
                return

            credentials = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            self.drive_service = build('drive', 'v3', credentials=credentials)
            print("✅ Google Drive verbunden!")
        except Exception as e:
            print(f"⚠️  Google Drive Fehler: {e}")
            self.drive_service = None

    def fetch_videos_from_drive(self):
        """Download videos from Google Drive"""
        if not self.drive_service or not self.raw_folder_id:
            print("⚠️  Google Drive nicht verfügbar. Checking local files...")
            return self._get_local_clips()

        print("\n🔍 Videos von Google Drive abrufen...")

        query = f"'{self.raw_folder_id}' in parents and trashed=false"
        results = self.drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)',
            pageSize=100
        ).execute()

        videos = [
            f for f in results.get('files', [])
            if 'video' in f['mimeType']
        ]

        print(f"📹 {len(videos)} Videos gefunden\n")

        downloaded = []
        for video in videos:
            local_path = self.local_raw / video['name']

            if local_path.exists():
                print(f"✅ {video['name']} (bereits lokal)")
                downloaded.append(local_path)
                continue

            print(f"⬇️  {video['name']}...")
            request = self.drive_service.files().get_media(fileId=video['id'])

            with open(local_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()

            print(f"✅ {video['name']} (heruntergeladen)")
            downloaded.append(local_path)

        return downloaded

    def _get_local_clips(self):
        """Get clips from local data/raw folder"""
        extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        clips = []
        for ext in extensions:
            clips.extend(self.local_raw.glob(f'*{ext}'))
        return sorted(clips)

    def process_videos(self, videos):
        """Process all videos through 5 phases"""
        if not videos:
            print("❌ Keine Videos gefunden!")
            return

        print("="*60)
        print("PHASE 2: SCHNEIDEN & OPTIMIEREN")
        print("="*60)

        processed = []
        for i, video_path in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] {video_path.name}")

            output_path = self.local_output / f"short_{i:03d}.mp4"

            if self._optimize_tiktok(str(video_path), str(output_path)):
                processed.append(output_path)
                print(f"   ✅ {output_path.name}")

        return processed

    def _optimize_tiktok(self, input_path, output_path):
        """Convert to TikTok 9:16 format"""
        try:
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)

            ret, frame = cap.read()
            if not ret:
                return False

            h, w = frame.shape[:2]

            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            out = cv2.VideoWriter(
                output_path, fourcc, fps,
                (self.config['tiktok_width'], self.config['tiktok_height'])
            )

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                aspect = w / h
                target_aspect = self.config['tiktok_width'] / self.config['tiktok_height']

                if aspect > target_aspect:
                    new_w = int(h * target_aspect)
                    x = (w - new_w) // 2
                    frame = frame[:, x:x+new_w]
                else:
                    new_h = int(w / target_aspect)
                    y = (h - new_h) // 2
                    frame = frame[y:y+new_h, :]

                frame = cv2.resize(frame, (self.config['tiktok_width'], self.config['tiktok_height']))
                frame = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
                out.write(frame)

            cap.release()
            out.release()

            return Path(output_path).exists()
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def generate_hooks_and_metadata(self, videos):
        """Generate descriptions, hashtags, tips"""
        print("\n" + "="*60)
        print("PHASE 4: HOOKS GENERIEREN")
        print("="*60)

        hooks = [
            "Dieser Beauty-Hack ist WILD 😍",
            "Warte bis zum Ende, das Ergebnis ist KRASS! ✨",
            "Das hätte ich nie erwartet... 💄",
            "Beauty Secret - probier es selbst! 💅",
            "Diese Transformation ist unreal 🌟",
        ]

        hashtags = [
            "#BeautyTok #MakeupTutorial #SkincareRoutine #BeautyHacks #MakeupArtist",
            "#BeautyCommunity #TikTok #Viral #FYP #ForYou",
            "#MakeupTips #BeautyTrends #Transformation #GlowUp #Tutorial",
        ]

        tips = [
            "🕐 Best time: 18:00-20:00",
            "📱 Use trending sounds",
            "❤️ Respond to comments",
            "🎯 Hook in first 2 seconds",
        ]

        metadata = {}

        for i, video in enumerate(videos, 1):
            video_name = video.stem

            metadata[video_name] = {
                'filename': video.name,
                'hook': hooks[i % len(hooks)],
                'hashtags': hashtags[i % len(hashtags)],
                'tip': tips[i % len(tips)],
            }

            # Create description file
            desc_file = video.with_suffix('.txt')
            with open(desc_file, 'w', encoding='utf-8') as f:
                f.write(f"""DESCRIPTION:
{metadata[video_name]['hook']}

HASHTAGS:
{metadata[video_name]['hashtags']}

TIP:
{metadata[video_name]['tip']}
""")

            print(f"\n[{i}] {video.name}")
            print(f"    📝 {metadata[video_name]['hook']}")

        # Save metadata
        with open(self.local_output / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return metadata

    def upload_to_drive(self):
        """Upload results back to Google Drive"""
        if not self.drive_service or not self.raw_folder_id:
            print("\n⚠️  Google Drive upload skipped (not configured)")
            return

        print("\n" + "="*60)
        print("📤 UPLOADING TO GOOGLE DRIVE")
        print("="*60)

        # Create output folder if it doesn't exist
        output_folder_name = "Beauty-TikTok-Output"

        # Find or create folder
        query = f"name='{output_folder_name}' and '{self.raw_folder_id}' in parents and trashed=false"
        results = self.drive_service.files().list(q=query, spaces='drive', fields='files(id)').execute()
        folders = results.get('files', [])

        if folders:
            output_folder_id = folders[0]['id']
        else:
            print(f"📁 Creating folder: {output_folder_name}")
            file_metadata = {
                'name': output_folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.raw_folder_id]
            }
            folder = self.drive_service.files().create(body=file_metadata, fields='id').execute()
            output_folder_id = folder.get('id')

        # Upload files
        for file_path in self.local_output.glob('short_*.mp4'):
            print(f"📤 {file_path.name}...")
            file_metadata = {'name': file_path.name, 'parents': [output_folder_id]}
            media = MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
            self.drive_service.files().create(body=file_metadata, media_body=media).execute()
            print(f"   ✅ Uploaded")

        for file_path in self.local_output.glob('short_*.txt'):
            print(f"📤 {file_path.name}...")
            file_metadata = {'name': file_path.name, 'parents': [output_folder_id]}
            media = MediaFileUpload(file_path, mimetype='text/plain')
            self.drive_service.files().create(body=file_metadata, media_body=media).execute()
            print(f"   ✅ Uploaded")

    def run(self):
        """Run complete workflow"""
        print("\n" + "🚀 "*30)
        print("BEAUTY TIKTOK SHORTS + GOOGLE DRIVE")
        print("🚀 "*30)

        # Phase 1: Fetch
        videos = self.fetch_videos_from_drive()

        if not videos:
            print("❌ No videos found!")
            return

        # Phase 2: Process
        processed = self.process_videos(videos)

        if not processed:
            print("❌ Processing failed!")
            return

        # Phase 4: Generate
        self.generate_hooks_and_metadata(processed)

        # Phase 5: Upload
        self.upload_to_drive()

        # Summary
        print("\n" + "="*60)
        print("✨ WORKFLOW FERTIG!")
        print("="*60)
        print(f"📊 Videos verarbeitet: {len(processed)}")
        print(f"📁 Lokal: data/processed/")
        print(f"📤 Google Drive: Beauty-TikTok-Output/")
        print("="*60 + "\n")

if __name__ == '__main__':
    processor = BeautyTikTokShortsWithDrive()
    processor.run()
