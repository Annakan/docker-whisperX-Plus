#!/usr/bin/env python3
"""
Simple test script for the WhisperX REST API.

This script tests the API endpoints to ensure they are working correctly.
"""

import sys
import time
import requests


def test_health_check(base_url: str = "http://localhost:8000"):
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Health check passed: {data}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False


def test_root_endpoint(base_url: str = "http://localhost:8000"):
    """Test the root endpoint."""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Root endpoint passed: {data}")
        return True
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
        return False


def test_transcribe_endpoint(base_url: str = "http://localhost:8000", audio_file: str = None):
    """Test the transcribe endpoint."""
    print("\nTesting transcribe endpoint...")
    
    if not audio_file:
        print("⚠ No audio file provided. Skipping transcribe test.")
        print("  To test transcription, provide an audio file path as argument:")
        print("  python test_api.py /path/to/audio.mp3")
        return None
    
    try:
        print(f"  Uploading file: {audio_file}")
        with open(audio_file, "rb") as f:
            files = {"audio": f}
            data = {
                "model": "tiny",  # Use tiny model for faster testing
                "language": "en",
                "output_format": "json"
            }
            
            print("  Transcribing... (this may take a while)")
            response = requests.post(f"{base_url}/transcribe", files=files, data=data)
            response.raise_for_status()
            result = response.json()
            
            print("✓ Transcription successful!")
            print(f"  Language detected: {result.get('language', 'N/A')}")
            print(f"  Number of segments: {len(result.get('segments', []))}")
            
            if result.get('segments'):
                print("\n  First few transcriptions:")
                for i, segment in enumerate(result['segments'][:3]):
                    print(f"    [{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}")
            
            return True
    except FileNotFoundError:
        print(f"✗ Audio file not found: {audio_file}")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e}")
        if e.response:
            print(f"  Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"✗ Transcription failed: {e}")
        return False


def wait_for_server(base_url: str = "http://localhost:8000", max_attempts: int = 10):
    """Wait for the server to become available."""
    print(f"Waiting for server at {base_url}...")
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✓ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"  Attempt {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("✗ Server did not become available")
    return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("WhisperX REST API Test Suite")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    audio_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Check if server is running
    if not wait_for_server(base_url):
        print("\n⚠ Server is not running. Please start it with:")
        print("  whisperx --serve")
        return 1
    
    # Run tests
    results = []
    results.append(("Health Check", test_health_check(base_url)))
    results.append(("Root Endpoint", test_root_endpoint(base_url)))
    transcribe_result = test_transcribe_endpoint(base_url, audio_file)
    if transcribe_result is not None:
        results.append(("Transcribe Endpoint", transcribe_result))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
