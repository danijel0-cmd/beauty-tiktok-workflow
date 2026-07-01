"""Hook Detection for TikTok Videos"""

import cv2
import numpy as np
import logging
from typing import List, Dict
import mediapipe as mp

logger = logging.getLogger(__name__)


class HookDetector:
    """Detect engaging moments (hooks) in beauty videos"""

    def __init__(self, config: dict):
        self.config = config
        self.min_length = config.get('hook_detection', {}).get('min_length', 1.0)
        self.max_length = config.get('hook_detection', {}).get('max_length', 3.0)
        self.motion_threshold = config.get('hook_detection', {}).get('motion_threshold', 0.4)
        self.scene_threshold = config.get('hook_detection', {}).get('scene_change_threshold', 25.0)

        # MediaPipe for face detection
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )

    def detect_hooks(self, video_path: str) -> List[Dict]:
        """Detect potential hooks in a video"""
        cap = cv2.VideoCapture(video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps

        logger.info(f"Video: {duration:.1f}s @ {fps:.0f}fps, {total_frames} frames")

        hooks = []
        prev_frame = None
        scene_changes = []

        frame_idx = 0

        while cap.isOpened() and frame_idx < total_frames:
            ret, frame = cap.read()
            if not ret:
                break

            timestamp = frame_idx / fps

            # Detect scene changes
            if prev_frame is not None:
                flow = self._detect_motion(prev_frame, frame)
                if flow > self.motion_threshold:
                    scene_changes.append({
                        'timestamp': timestamp,
                        'motion': flow
                    })

            # Detect face expressions/attention
            faces = self._detect_faces(frame)
            if faces and len(faces) > 0:
                for face in faces:
                    confidence = face.get('confidence', 0)
                    if confidence > 0.7:
                        hooks.append({
                            'start': max(0, timestamp - 0.5),
                            'end': min(duration, timestamp + 2.0),
                            'confidence': confidence,
                            'type': 'face_attention',
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

    def _detect_faces(self, frame: np.ndarray) -> List[Dict]:
        """Detect faces and eye gaze using MediaPipe"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detector.process(rgb_frame)

        faces = []
        if results.detections:
            for detection in results.detections:
                faces.append({
                    'confidence': detection.score[0],
                    'bbox': detection.location_data.bounding_box if hasattr(
                        detection.location_data, 'bounding_box'
                    ) else None
                })

        return faces

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
