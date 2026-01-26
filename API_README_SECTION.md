# REST API Server

WhisperX now includes a built-in REST API server that exposes all transcription functionality via HTTP endpoints.

## Quick Start

Start the API server:

```bash
whisperx --serve
```

The server will start on `http://localhost:8000` by default.

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Basic Usage Example

```bash
# Transcribe an audio file
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio=@audio.mp3" \
  -F "model=base" \
  -F "language=en"
```

## Python Example

```python
import requests

url = "http://localhost:8000/transcribe"
files = {"audio": open("audio.mp3", "rb")}
data = {"model": "base", "language": "en"}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result["segments"])
```

## Server Options

```bash
whisperx --serve --host 127.0.0.1 --port 9000 --workers 2 --log-level debug

Options:
  --host TEXT        Host to bind the server to (default: 0.0.0.0)
  --port INTEGER     Port to bind the server to (default: 8000)
  --workers INTEGER  Number of worker processes (default: 1)
  --log-level TEXT   Logging level: debug, info, warning, error, critical
```

## Features

- **Full CLI Parity**: All CLI parameters are available as API form fields
- **Automatic Documentation**: Interactive Swagger UI and ReDoc interfaces
- **File Upload**: Direct audio file upload via multipart/form-data
- **JSON Responses**: Structured JSON output with segments and word-level timestamps
- **Production Ready**: Built on FastAPI and Uvicorn for high performance

## Complete Documentation

For detailed API documentation, usage examples, and parameter reference, see [API_USAGE.md](API_USAGE.md).

## Testing

A test script is provided to verify the API:

```bash
# Test basic endpoints
python test_api.py

# Test with transcription
python test_api.py /path/to/audio.mp3
```
