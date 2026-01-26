# WhisperX REST API Usage

This document describes how to use the WhisperX REST API server.

## Starting the Server

To start the REST API server, use the `--serve` flag:

```bash
whisperx --serve
```

### Server Options

- `--host`: Host to bind the server to (default: `0.0.0.0`)
- `--port`: Port to bind the server to (default: `8000`)
- `--workers`: Number of worker processes (default: `1`)
- `--log-level`: Logging level - choices: debug, info, warning, error, critical (default: `info`)

Example:

```bash
whisperx --serve --host 127.0.0.1 --port 9000 --workers 2 --log-level debug
```

## API Endpoints

### Health Check

**GET** `/health`

Returns the health status of the server.

**Response:**
```json
{
  "status": "healthy"
}
```

### Root Endpoint

**GET** `/`

Returns API information.

**Response:**
```json
{
  "name": "WhisperX API",
  "version": "1.0.0",
  "endpoints": {
    "/transcribe": "POST - Transcribe audio file with WhisperX"
  }
}
```

### Transcribe Audio

**POST** `/transcribe`

Transcribe an audio file with WhisperX. This endpoint accepts the same parameters as the CLI transcribe command.

**Request:** `multipart/form-data`

**Required Parameters:**
- `audio`: Audio file to transcribe (file upload)

**Optional Parameters:**

All CLI parameters are supported as form fields. Here are the most common ones:

- `model`: Name of the Whisper model to use (default: `small`)
- `language`: Language spoken in the audio (e.g., `en`, `es`, `fr`, etc.)
- `task`: Task to perform - `transcribe` or `translate` (default: `transcribe`)
- `output_format`: Format of the output - `json`, `srt`, `vtt`, `txt`, `tsv`, `aud` (default: `json`)
- `batch_size`: Preferred batch size for inference (default: `8`)
- `device`: Device to use - `cuda` or `cpu` (default: auto-detect)
- `compute_type`: Compute type - `float16`, `float32`, `int8` (default: `float16`)

**Alignment Parameters:**
- `no_align`: Do not perform phoneme alignment (default: `false`)
- `align_model`: Name of phoneme-level ASR model to do alignment
- `interpolate_method`: Method to assign timestamps - `nearest`, `linear`, `ignore` (default: `nearest`)
- `return_char_alignments`: Return character-level alignments (default: `false`)

**VAD Parameters:**
- `vad_method`: VAD method - `pyannote` or `silero` (default: `pyannote`)
- `vad_onset`: Onset threshold for VAD (default: `0.500`)
- `vad_offset`: Offset threshold for VAD (default: `0.363`)
- `chunk_size`: Chunk size for merging VAD segments (default: `30`)

**Diarization Parameters:**
- `diarize`: Apply diarization to assign speaker labels (default: `false`)
- `min_speakers`: Minimum number of speakers
- `max_speakers`: Maximum number of speakers
- `diarize_model`: Name of the speaker diarization model (default: `pyannote/speaker-diarization-3.1`)
- `speaker_embeddings`: Include speaker embeddings in output (default: `false`)

**Decoding Parameters:**
- `temperature`: Temperature to use for sampling (default: `0`)
- `best_of`: Number of candidates when sampling (default: `5`)
- `beam_size`: Number of beams in beam search (default: `5`)
- `patience`: Patience value in beam decoding (default: `1.0`)
- `initial_prompt`: Optional text prompt for the first window

**Response:**
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello, this is a test.",
      "words": [
        {
          "word": "Hello",
          "start": 0.0,
          "end": 0.5,
          "score": 0.95
        },
        ...
      ]
    }
  ],
  "language": "en",
  "word_segments": [...]
}
```

## Usage Examples

### Using cURL

```bash
# Basic transcription
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio=@/path/to/audio.mp3" \
  -F "model=base" \
  -F "language=en"

# With diarization
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio=@/path/to/audio.mp3" \
  -F "model=large-v3" \
  -F "language=en" \
  -F "diarize=true" \
  -F "min_speakers=2" \
  -F "max_speakers=4"

# Translation to English
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio=@/path/to/audio.mp3" \
  -F "model=medium" \
  -F "task=translate"
```

### Using Python

```python
import requests

# Basic transcription
url = "http://localhost:8000/transcribe"
files = {"audio": open("audio.mp3", "rb")}
data = {
    "model": "base",
    "language": "en",
    "output_format": "json"
}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result)
```

### Using Python with requests

```python
import requests

def transcribe_audio(audio_path, model="base", language="en"):
    url = "http://localhost:8000/transcribe"
    
    with open(audio_path, "rb") as audio_file:
        files = {"audio": audio_file}
        data = {
            "model": model,
            "language": language,
            "output_format": "json"
        }
        
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()

# Usage
result = transcribe_audio("my_audio.mp3", model="large-v3", language="en")
for segment in result["segments"]:
    print(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}")
```

## Interactive API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

These interfaces allow you to explore the API, see all available parameters, and test requests directly from your browser.

## Notes

- The API accepts all the same parameters as the CLI, ensuring feature parity
- All audio file formats supported by the CLI are supported by the API
- The server runs on GPU if available, falling back to CPU automatically
- For production use, consider increasing `--workers` for better performance
- The server processes one request at a time per worker
- Large files may take time to process; consider setting appropriate timeout values in your client

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful transcription
- `400 Bad Request`: Invalid audio file or parameters
- `500 Internal Server Error`: Transcription processing error

Error responses include a `detail` field with information about what went wrong.

Example error response:
```json
{
  "detail": "Transcription failed: Invalid audio format"
}
```
