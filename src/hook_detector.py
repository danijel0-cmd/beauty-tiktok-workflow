"""Hook Detection for TikTok Videos"""

import cv2
import numpy as np
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class HookDetector:
    """Detect engaging moments (hooks) in beauty videos"""

    def __init__(self, config: dict):
        self.config = config
        self.min_length = config.get('hook_detection', {}).get('min_length', 1.0)
        self.max_length = config.get('hook_detection', {}).get('max_length', 3.0)
        self.motion_threshold = config.get('hook_detection', {}).get('motion_threshold', 0.4)
        self.scene_threshold = config.get('hook_detection', {}).get('scene_change_threshold', 25.0)

    def detect_hooks(self, video_path: str) -> List[Dict]:
        """Detect potential hooks in a video using motion detection"""
        cap = cv2.VideoCapture(video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps

        logger.info(f"Video: {duration:.1f}s @ {fps:.0f}fps, {total_frames} frames")

        hooks = []
        prev_frame = None
        frame_idx = 0
        sample_rate = max(1, int(fps / 2))  # Check every 0.5s

        while cap.isOpened() and frame_idx < total_frames:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % sample_rate != 0:
                frame_idx += 1
                continue

            timestamp = frame_idx / fps

            # Detect motion/scene changes
            if prev_frame is not None:
                motion = self._detect_motion(prev_frame, frame)
                if motion > self.motion_threshold:
                    hooks.append({
                        'start': max(0, timestamp - 1.0),
                        'end': min(duration, timestamp + 2.0),
                        'confidence': min(motion / 5.0, 1.0),
                        'type': 'motion',
                        'timestamp': timestamp
                    })

            prev_frame = frame.copy()
            frame_idx += 1

        cap.release()

        # Filter and merge overlapping hooks
        hooks = self._merge_overlapping_hooks(hooks)
        hooks = sorted(hooks, key=lambda h: h['confidence'], reverse=True)

        logger.info(f"Detected {len(hooks)} hooks")
        for i, hook in enumerate(hooks[:3]):
            logger.debug(
                f"Hook {i+1}: {hook['start']:.1f}s - {hook['end']:.1f}s "
                f"(confidence: {hook['confidence']:.2f})"
            )

        return hooks[:5]  # Return top 5 hooks

    def _detect_motion(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Calculate optical flow between frames"""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(
            gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )

        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        return np.mean(magnitude)


    def _merge_overlapping_hooks(self, hooks: List[Dict]) -> List[Dict]:
        """Merge overlapping hook timestamps"""
        if not hooks:
            return []

        merged = []
        sorted_hooks = sorted(hooks, key=lambda h: h['start'])

        current = sorted_hooks[0].copy()

        for hook in sorted_hooks[1:]:
            if hook['start'] <= current['end']:
                current['end'] = max(current['end'], hook['end'])
                current['confidence'] = max(current['confidence'], hook['confidence'])
            else:
                if current['end'] - current['start'] >= self.min_length:
                    merged.append(current)
                current = hook.copy()

        if current['end'] - current['start'] >= self.min_length:
            merged.append(current)

        return merged
