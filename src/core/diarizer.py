import os
import logging
from typing import List, Dict
import torch

# Try importing pyannote, handle failure gracefully
try:
    from pyannote.audio import Pipeline
    PYANNOTE_AVAILABLE = True
except ImportError:
    PYANNOTE_AVAILABLE = False

try:
    from src.utils.logger import setup_logger
    logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class DiarizationEngine:
    def __init__(self, use_auth_token: str = None):
        self.token = use_auth_token or os.getenv("HF_TOKEN")
        self.pipeline = None
        
        if self.token and PYANNOTE_AVAILABLE:
            logger.info("Loading Pyannote Diarization pipeline...")
            try:
                self.pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization",
                    use_auth_token=self.token
                )
            except Exception as e:
                logger.warning(f"Could not load Pyannote pipeline: {e}. Switching to Mock Mode.")
        else:
            logger.warning("No HF_TOKEN found or Pyannote not installed. Running in MOCK MODE.")

    def process(self, audio_path: str) -> List[Dict]:
        """
        Returns list of segments: [{'start': 0.0, 'end': 1.0, 'speaker': 'SPEAKER_00'}]
        """
        if self.pipeline:
            # Real processing
            logger.info(f"Diarizing {audio_path}...")
            diarization = self.pipeline(audio_path)
            results = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                results.append({
                    "start": turn.start,
                    "end": turn.end,
                    "speaker": speaker
                })
            return results
        else:
            # Mock processing for demo/testing without credentials
            logger.info("Generating mock diarization data...")
            return self._generate_mock_diarization(audio_path)

    def _generate_mock_diarization(self, audio_path: str) -> List[Dict]:
        # Simulates 2 speakers alternating every 5 seconds
        import librosa
        duration = librosa.get_duration(path=audio_path)
        segments = []
        curr = 0.0
        speaker_idx = 0
        while curr < duration:
            end = min(curr + 5.0, duration)
            segments.append({
                "start": curr,
                "end": end,
                "speaker": f"SPEAKER_0{speaker_idx % 2 + 1}"
            })
            curr = end
            speaker_idx += 1
        return segments
