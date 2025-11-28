import logging
import os
from typing import List, Dict, Any
from faster_whisper import WhisperModel

# Fallback logger
try:
    from src.utils.logger import setup_logger
    logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class ASREngine:
    """
    Wrapper for Faster-Whisper ASR model.
    """
    def __init__(self, model_size: str = "medium", device: str = "cpu"):
        self.model_size = model_size
        self.device = device
        logger.info(f"Loading Whisper model: {model_size} on {device}...")
        try:
            self.model = WhisperModel(model_size, device=device, compute_type="int8")
        except Exception as e:
            logger.error(f"Failed to load Whisper: {e}")
            self.model = None

    def transcribe(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Transcribes audio file to text segments with timestamps.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        logger.info(f"Transcribing {audio_path}...")
        
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        results = []
        for segment in segments:
            results.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
            
        logger.info(f"Transcription complete. Detected language: {info.language}")
        return results
