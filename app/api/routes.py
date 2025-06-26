# app/api/routes.py

import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from app.core.config import settings
from app.utils.helpers import save_upload_file, create_output_path
from app.core.tasks import process_pdf_task
from app.utils.logger import logger

router = APIRouter()

@router.post("/upload/")
async def upload_and_translate(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported."})

    try:
        # Save uploaded PDF
        input_path = save_upload_file(settings.TEMP_DIR, file)
        output_path = create_output_path(settings.TEMP_DIR, file.filename)

        # Launch translation as a background task
        process_pdf_task.delay(input_path, output_path)

        logger.info(f"Translation task launched for: {file.filename}")

        return JSONResponse(
            status_code=202,
            content={
                "message": "Translation started. You can download the result when it's ready.",
                "input_file": input_path,
                "output_file": output_path
            }
        )

    except Exception as e:
        logger.error(f"Upload error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "File upload failed.", "details": str(e)}
        )

@router.get("/download/")
def download_translated(file_path: str):
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "Translated file not ready."})

    return FileResponse(file_path, media_type="application/pdf", filename=os.path.basename(file_path))