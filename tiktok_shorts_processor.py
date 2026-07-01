#!/usr/bin/env python3
"""
Professional TikTok Shorts Workflow
Auto-process raw clips → optimized shorts + hooks + hashtags
"""

import cv2
import os
from pathlib import Path
import json
from datetime import datetime
from tqdm import tqdm

class BeautyTikTokShorts:
    """Production-grade shorts processor"""

    def __init__(self, input_dir="data/raw", output_dir="data/processed"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.config = {
            'tiktok_width': 1080,
            'tiktok_height': 1920,
            'fps': 30,
            'bitrate': '8M',
            'max_duration': 60  # TikTok max
        }

    def get_input_clips(self):
        """Get all video clips from input directory"""
        extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        clips = []

        for ext in extensions:
            clips.extend(self.input_dir.glob(f'*{ext}'))

        return sorted(clips)

    def phase1_prepare_clips(self, clips):
        """PHASE 1: Prepare and list clips"""
        print("\n" + "="*60)
        print("PHASE 1: CLIPS VORBEREITEN")
        print("="*60)

        for i, clip in enumerate(clips, 1):
            cap = cv2.VideoCapture(str(clip))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frames / fps
            cap.release()

            print(f"  [{i}] {clip.name}: {duration:.1f}s @ {fps:.0f}fps")

        return clips

    def phase2_cut_optimize(self, clips):
        """PHASE 2: Schneiden + Optimieren für TikTok"""
        print("\n" + "="*60)
        print("PHASE 2: SCHNEIDEN & OPTIMIEREN")
        print("="*60)

        processed_videos = []

        for i, clip_path in enumerate(clips, 1):
            print(f"\n  [{i}/{len(clips)}] Verarbeite: {clip_path.name}")

            output_path = self.output_dir / f"short_{i:03d}.mp4"

            if self._optimize_for_tiktok(str(clip_path), str(output_path)):
                processed_videos.append(output_path)
                print(f"     ✅ Optimiert: {output_path.name}")

        return processed_videos

    def _optimize_for_tiktok(self, input_path, output_path):
        """Convert to TikTok format (1080x1920, 9:16)"""
        try:
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)

            ret, first_frame = cap.read()
            if not ret:
                return False

            h, w = first_frame.shape[:2]

            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            out = cv2.VideoWriter(
                output_path,
                fourcc,
                fps,
                (self.config['tiktok_width'], self.config['tiktok_height'])
            )

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Resize to 9:16 aspect ratio
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

                # Brightness/contrast optimization
                frame = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)

                out.write(frame)
                frame_count += 1

            cap.release()
            out.release()

            return Path(output_path).exists()
        except Exception as e:
            print(f"     ❌ Error: {e}")
            return False

    def phase3_effects_placeholder(self, videos):
        """PHASE 3: Effekte (Platzhalter - CapCut macht das)"""
        print("\n" + "="*60)
        print("PHASE 3: EFFEKTE")
        print("="*60)
        print("  ℹ️  CapCut übernimmt die Effekte - Videos vorbereitet")
        return videos

    def phase4_generate_hooks(self, videos):
        """PHASE 4: Hooks generieren (Text für Beschreibung)"""
        print("\n" + "="*60)
        print("PHASE 4: HOOKS GENERIEREN")
        print("="*60)

        beauty_hooks = [
            "Dieser Beauty-Hack ist WILD 😍",
            "Warte bis zum Ende, das Ergebnis ist KRASS! ✨",
            "Das hätte ich nie erwartet... 💄",
            "Beauty Secret #1 - probier es selbst aus! 💅",
            "Diese Transformation ist unreal 🌟",
            "Schau wie einfach das ist! 💋",
            "Das ist mein neuer Favorit-Trick 🎀",
            "Dein Makeup-Game wird sich ändern 💫",
            "Tag jemanden, der das braucht! 👇",
            "Tutorial folgt - speicher dir das! 📌",
        ]

        hashtags = [
            "#BeautyTok #MakeupTutorial #SkincareRoutine #BeautyHacks #MakeupArtist",
            "#BeautyCommunity #TikTok #Viral #FYP #ForYou",
            "#MakeupTips #BeautyTrends #Transformation #GlowUp #Tutorial",
            "#ShortForm #ContentCreator #BeautyChannel #TikTokMakeup #SocialMedia"
        ]

        tips = [
            "🕐 Best time to post: 18:00-20:00 (peak engagement)",
            "📱 Use trending sounds for 40% more views",
            "❤️ Respond to comments in first hour",
            "🎯 Hook in first 2 seconds or they scroll",
            "📊 Post consistently (3-5x per week)"
        ]

        hooks_data = {}

        for i, video in enumerate(videos, 1):
            video_name = video.stem

            hooks_data[video_name] = {
                'filename': video.name,
                'created': datetime.now().isoformat(),
                'hooks': beauty_hooks[i % len(beauty_hooks):(i % len(beauty_hooks)) + 2],
                'hashtags': hashtags[i % len(hashtags)],
                'tips': tips[i % len(tips)],
            }

            print(f"\n  [{i}] {video.name}")
            print(f"     📝 Hook: {hooks_data[video_name]['hooks'][0]}")
            print(f"     #️⃣  Tags: {hooks_data[video_name]['hashtags'][:40]}...")
            print(f"     💡 Tip: {hooks_data[video_name]['tips']}")

        # Save metadata
        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(hooks_data, f, indent=2, ensure_ascii=False)

        print(f"\n  ✅ Metadata gespeichert: {metadata_path}")

        return hooks_data

    def phase5_export_ready(self, videos, metadata):
        """PHASE 5: Export-ready (alles zusammen)"""
        print("\n" + "="*60)
        print("PHASE 5: EXPORT READY")
        print("="*60)

        for i, video in enumerate(videos, 1):
            video_name = video.stem
            meta = metadata.get(video_name, {})

            # Create description file for easy copy-paste
            desc_file = video.with_suffix('.txt')

            description = f"""
DESCRIPTION:
{meta.get('hooks', [''])[0]}

HASHTAGS:
{meta.get('hashtags', '')}

TIP:
{meta.get('tips', '')}

---
Video: {video.name}
Größe: {video.stat().st_size / (1024*1024):.1f} MB
Ready: {datetime.now().isoformat()}
""".strip()

            with open(desc_file, 'w', encoding='utf-8') as f:
                f.write(description)

            print(f"\n  [{i}] {video.name}")
            print(f"     📍 Video: {video}")
            print(f"     📋 Description: {desc_file}")

    def run(self):
        """Run complete workflow"""
        print("\n" + "🚀 "*30)
        print("BEAUTY TIKTOK SHORTS WORKFLOW - PRODUCTION")
        print("🚀 "*30)

        # Phase 1: Get clips
        clips = self.phase1_prepare_clips(self.get_input_clips())

        if not clips:
            print("❌ Keine Clips gefunden!")
            return

        # Phase 2: Optimize
        videos = self.phase2_cut_optimize(clips)

        if not videos:
            print("❌ Fehler beim Optimieren!")
            return

        # Phase 3: Effects (placeholder)
        videos = self.phase3_effects_placeholder(videos)

        # Phase 4: Generate hooks
        metadata = self.phase4_generate_hooks(videos)

        # Phase 5: Export ready
        self.phase5_export_ready(videos, metadata)

        # Summary
        print("\n" + "="*60)
        print("✨ WORKFLOW FERTIG!")
        print("="*60)
        print(f"📁 Output Ordner: {self.output_dir}")
        print(f"📊 Videos verarbeitet: {len(videos)}")
        print(f"📋 Metadata: {self.output_dir / 'metadata.json'}")
        print("\nNächste Schritte:")
        print("  1. Videos in CapCut öffnen (für Effekte)")
        print("  2. Descriptions aus .txt files kopieren")
        print("  3. Hochladen & Posten!")
        print("="*60 + "\n")

if __name__ == '__main__':
    processor = BeautyTikTokShorts()
    processor.run()
