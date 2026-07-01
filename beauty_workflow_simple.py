#!/usr/bin/env python3
"""Beauty TikTok Workflow - Simplified Version (OpenCV)"""

import cv2
import sys
from pathlib import Path
from tqdm import tqdm

def analyze_video(video_path):
    """Analyze video for motion/hooks"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"📹 Video: {duration:.1f}s @ {fps:.0f}fps")

    prev_frame = None
    hooks = []
    frame_idx = 0
    sample_rate = max(1, int(fps / 2))

    while cap.isOpened() and frame_idx < total_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % sample_rate == 0:
            timestamp = frame_idx / fps

            if prev_frame is not None:
                gray1 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(
                    gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0
                )
                magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
                motion = magnitude.mean()

                if motion > 0.4:
                    hooks.append({
                        'timestamp': timestamp,
                        'motion': float(motion),
                        'start': max(0, timestamp - 1.0),
                        'end': min(duration, timestamp + 2.5)
                    })

            prev_frame = frame.copy()

        frame_idx += 1

    cap.release()

    hooks = sorted(hooks, key=lambda h: h['motion'], reverse=True)[:3]

    print(f"🎯 Found {len(hooks)} hooks:")
    for i, hook in enumerate(hooks, 1):
        print(f"   Hook {i}: {hook['start']:.1f}s - {hook['end']:.1f}s (motion: {hook['motion']:.2f})")

    return hooks, duration, fps

def extract_hook_frames(input_path, hook, fps, output_path):
    """Extract hook frames and save as video"""
    print(f"\n✂️ Extracting hook ({hook['start']:.1f}s - {hook['end']:.1f}s)...")

    cap = cv2.VideoCapture(input_path)

    start_frame = int(hook['start'] * fps)
    end_frame = int(hook['end'] * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    ret, first_frame = cap.read()
    if not ret:
        print("❌ Could not read first frame")
        return False

    h, w = first_frame.shape[:2]
    target_h = 1920
    target_w = 1080

    print(f"   Input: {w}x{h}, Output: {target_w}x{target_h}")

    # Try different codecs
    codecs = ['mp4v', 'avc1', 'MJPG', 'DIVX']
    out = None

    for codec in codecs:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(output_path, fourcc, fps, (target_w, target_h))
            if out.isOpened():
                print(f"   Using codec: {codec}")
                break
            out.release()
        except Exception as e:
            print(f"   Codec {codec} failed: {e}")
            continue

    if out is None or not out.isOpened():
        print("❌ Could not initialize VideoWriter")
        cap.release()
        return False

    frames_to_extract = end_frame - start_frame
    print(f"   Extracting {frames_to_extract} frames...")

    for frame_count in tqdm(range(frames_to_extract), desc="Cutting"):
        ret, frame = cap.read()
        if not ret:
            break

        # Resize to TikTok format
        aspect = w / h
        target_aspect = target_w / target_h

        if aspect > target_aspect:
            new_w = int(h * target_aspect)
            x_start = (w - new_w) // 2
            frame = frame[:, x_start:x_start + new_w]
        else:
            new_h = int(w / target_aspect)
            y_start = (h - new_h) // 2
            frame = frame[y_start:y_start + new_h, :]

        frame = cv2.resize(frame, (target_w, target_h))
        out.write(frame)

    cap.release()
    out.release()

    # Verify file was created
    if Path(output_path).exists():
        size = Path(output_path).stat().st_size
        print(f"✅ Hook extracted: {output_path} ({size / (1024*1024):.1f} MB)")
        return True
    else:
        print(f"❌ Failed to write video file")
        return False

def main():
    input_video = "data/raw/beauty-video.mp4"
    output_video = "data/processed/tiktok_beauty.mp4"

    if not Path(input_video).exists():
        print(f"❌ Video not found: {input_video}")
        sys.exit(1)

    Path("data/processed").mkdir(parents=True, exist_ok=True)

    print("🚀 Beauty TikTok Auto-Workflow\n")

    hooks, duration, fps = analyze_video(input_video)

    if hooks:
        success = extract_hook_frames(input_video, hooks[0], fps, output_video)
    else:
        print("⚠️ No hooks found, using first 10 seconds")
        hook = {'start': 0, 'end': min(10, duration)}
        success = extract_hook_frames(input_video, hook, fps, output_video)

    if success:
        print(f"\n{'='*50}")
        print(f"✨ Fertig!")
        print(f"📍 Output: {output_video}")
        print(f"📱 Format: 1080x1920 (9:16 TikTok)")
        print(f"{'='*50}")

        # Open in Finder
        import os
        os.system(f"open {Path(output_video).parent}")
    else:
        print("❌ Failed to create video")
        sys.exit(1)

if __name__ == '__main__':
    main()
