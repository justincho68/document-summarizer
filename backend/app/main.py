from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Document Summarizer API"}

@app.post("/summarize")
async def summarize_document(file: UploadFile = File(...)):
    # This is just a placeholder - you'll implement the actual summarization later
    return {"filename": file.filename, "summary": "This is a sample summary."}