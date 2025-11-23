import os
import logging
from pathlib import Path
from typing import List, Optional
from pydub import AudioSegment
from pydub.utils import make_chunks

# Import our logger (assuming you created src/utils/logger.py)
# If that import fails, remove it and use: logging.basicConfig(level=logging.INFO)
try:
    from src.utils.logger import setup_logger
    logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class AudioProcessor:
    """
    Handles ingestion, normalization, and chunking of raw audio files
    for downstream AI processing.
    """

    def __init__(self, output_dir: str = "data/processed_audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Standard configuration for Whisper/ASR models
        self.target_sample_rate = 16000 
        self.target_channels = 1  # Mono

    def process_audio(self, file_path: str, chunk_length_ms: int = 600000) -> List[str]:
        """
        Main pipeline: Load -> Convert -> Normalize -> Chunk -> Save.
        
        Args:
            file_path: Path to the raw input file.
            chunk_length_ms: Length of chunks in milliseconds (default 10 mins).
            
        Returns:
            List of paths to the processed chunk files.
        """
        path_obj = Path(file_path)
        if not path_obj.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Input file not found: {file_path}")

        logger.info(f"Starting processing for: {file_path}")
        
        try:
            # 1. Load Audio
            audio = self._load_audio(path_obj)
            
            # 2. Convert to 16k Mono (Standard for Whisper)
            audio = audio.set_frame_rate(self.target_sample_rate).set_channels(self.target_channels)
            
            # 3. Export Chunks (to avoid OOM on large files)
            chunk_paths = self._export_chunks(audio, path_obj.stem, chunk_length_ms)
            
            logger.info(f"Successfully processed {len(chunk_paths)} chunks for {path_obj.name}")
            return chunk_paths
            
        except Exception as e:
            logger.error(f"Error processing audio {file_path}: {str(e)}")
            raise e

    def _load_audio(self, path_obj: Path) -> AudioSegment:
        """Loads audio based on file extension."""
        ext = path_obj.suffix.lower()
        if ext == ".mp3":
            return AudioSegment.from_mp3(str(path_obj))
        elif ext == ".wav":
            return AudioSegment.from_wav(str(path_obj))
        elif ext == ".m4a":
            return AudioSegment.from_file(str(path_obj), "m4a")
        else:
            # Fallback for other ffmpeg supported formats
            return AudioSegment.from_file(str(path_obj))

    def _export_chunks(self, audio: AudioSegment, base_filename: str, chunk_length_ms: int) -> List[str]:
        """Splits audio into chunks and saves them."""
        chunks = make_chunks(audio, chunk_length_ms)
        saved_paths = []
        
        for i, chunk in enumerate(chunks):
            chunk_name = f"{base_filename}_part_{i}.wav"
            out_path = self.output_dir / chunk_name
            
            # Export as WAV (PCM_16)
            chunk.export(str(out_path), format="wav")
            saved_paths.append(str(out_path))
            
        return saved_paths

if __name__ == "__main__":
    # Quick test execution
    processor = AudioProcessor()
    # Ensure you have a dummy file in data/raw_audio to test this!
    # processor.process_audio("data/raw_audio/test_meeting.mp3")
