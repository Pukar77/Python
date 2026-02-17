from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse
import assemblyai as aai
import tempfile
from dotenv import load_dotenv
import os
import logging

load_dotenv()

router = APIRouter(prefix="/convert", tags=["Speech to Text"])

ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
if not ASSEMBLY_API_KEY:
    raise RuntimeError("ASSEMBLY_API_KEY is not set")

aai.settings.api_key = ASSEMBLY_API_KEY
logger = logging.getLogger(__name__)

@router.post("/speech2text")
async def audio_creation(file: UploadFile = File(...)):
    tmp_path = None

    try:
        # Check if file was provided
        if not file:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": 0,
                    "message": "Validation failed. Please check your input.",
                    "errors": {"title": ["No audio file provided"]}
                }
            )

        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            if not content:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "status": 0,
                        "message": "Validation failed. Please check your input.",
                        "errors": {"title": ["Uploaded file is empty"]}
                    }
                )
            tmp.write(content)
            tmp_path = tmp.name

        # Configure AssemblyAI transcriber
        config = aai.TranscriptionConfig(speech_models=["universal"])
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(tmp_path)

        # Check transcription status
        if transcript.status == "error":
            logger.error("AssemblyAI error: %s", transcript.error)
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content={
                    "status": 0,
                    "message": "Validation failed. Please check your input.",
                    "errors": {"title": [f"Transcription failed: {transcript.error}"]}
                }
            )

        if not transcript.text:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content={
                    "status": 0,
                    "message": "Validation failed. Please check your input.",
                    "errors": {"title": ["Transcription completed but no text was returned"]}
                }
            )

        # Success response
        return {"text": transcript.text}

    except aai.AssemblyAIError as e:
        logger.exception("AssemblyAI SDK error")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "status": 0,
                "message": "Validation failed. Please check your input.",
                "errors": {"title": ["Speech-to-text service error"]}
            }
        )

    except Exception as e:
        logger.exception("Unexpected server error")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": 0,
                "message": "Validation failed. Please check your input.",
                "errors": {"title": ["Internal server error"]}
            }
        )

    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                logger.warning("Failed to delete temp file: %s", tmp_path)
