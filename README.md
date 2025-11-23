# Meeting Minutes Neural Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange.svg)
![Status](https://img.shields.io/badge/Status-Prototype-yellow)

## Overview
This project is an enterprise-grade, multi-modal pipeline designed to transform raw meeting audio into structured, actionable business intelligence. Unlike standard speech-to-text tools, this pipeline utilizes a **Neural approach** to speaker diarization, semantic topic segmentation, and intent classification (decisions vs. action items) before passing data to an LLM for final synthesis.

## Technical Architecture

```mermaid
graph TD
    A[Raw Audio Input] --> B[Audio Preprocessing/FFmpeg]
    B --> C{Parallel Processing}
    C -->|Stream 1| D[ASR: Faster-Whisper]
    C -->|Stream 2| E[Diarization: Pyannote.audio]
    D --> F[Alignment Engine]
    E --> F
    F --> G[Speaker-Labeled Transcript]
    G --> H[BERT Classifiers]
    H -->|Detect| I[Action Items & Decisions]
    G --> J[LLM Enrichment Layer]
    I --> J
    J --> K[Final JSON Output]