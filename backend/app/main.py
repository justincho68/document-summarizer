from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json

from app.utils.file_handler import save_upload_file, clean_up_file
from app.utils.document_processor import extract_text, preprocess_text, advanced_preprocess, fix_spacing_issue
from app.utils.summarizer import Summarizer

app = FastAPI()

origins = ["https://document-summarizer-1.onrender.com"]

summarizer = Summarizer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Request Origin: {request.headers.get('origin')}")
    logger.info(f"Headers: {request.headers}")
    
    response = await call_next(request)
    
    # Log response info
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response CORS headers: {response.headers.get('access-control-allow-origin')}")
    
    return response

@app.get("/")
def read_root():
    return {"message": "Document Summarizer API"}

@app.post("/extract")
#File(...) allows the backend to be expecting a file to come from file upload component
async def extract_document_text(file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file provided")
    #ensure that the file extension is valid
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.pdf', '.docx', '.txt']:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_extension}")
    try:
        #temporarily save the file
        #asynchronously save the file to a a temporary location so it can be worked on
        file_path = await save_upload_file(file)
        text = extract_text(file_path)
        #preprocess the file
        processed_text = preprocess_text(text)
        #clean the temporary file
        clean_up_file(file_path)
        return {
            "filename": file.filename,
            "text_length": len(processed_text),
            "text_preview": processed_text[:500] + "..." if len(processed_text) > 500 else processed_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/summarize")
async def summarize_document(
    file: UploadFile = File(...),
    method: str = Form("hybrid"),
    max_length: int = Form(150),
    min_length: int = Form(50),
    ratio: float = Form(0.3)
    ):
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "https://document-summarizer-1.onrender.com"
    # This is just a placeholder - you'll implement the actual summarization later
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file provided")
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.pdf', '.docx', '.txt']:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_extension}")
    #save as temp file
    try:
        print(f"📥 Received file: {file.filename}")
        file_path = await save_upload_file(file)
        print(f"📄 File saved at: {file_path}")
        text = extract_text(file_path)
        print(f"✂️ Extracted text: {text[:200]}...")
        processed_text = preprocess_text(text)
        from app.utils.document_processor import fix_spacing_issue
        processed_text = fix_spacing_issue(processed_text)
        print(f"🔧 Preprocessed text length: {len(processed_text)}")

        #create summary based on the method
        if method == "extractive":
            summary = summarizer.extractive_summarize(processed_text, ratio=ratio)
            summary_type = "Extractive"
        elif method == "abstractive":
            summary = summarizer.abstractive_summarize(
                processed_text, max_length=max_length, min_length=min_length
            )
            summary_type = "Abstractive"
        else:
            summaries = summarizer.hybrid_summarize(
                processed_text, max_length=max_length, min_length=min_length, ratio=ratio
            )
            summary = summaries["abstractive_summary"]
            summary_type = "Hybrid"
        clean_up_file(file_path)

        result = {
            "filename": file.filename,
            "text_length": len(processed_text),
            "summary_type": summary_type,
            "summary": summary
        }
        return JSONResponse(
            content=result,
            headers={
                "Access-Control-Allow-Origin": "https://document-summarizer-1.onrender.com",
                "Access-Control-Allow-Credentials": "true"
            }
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
