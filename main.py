from fastapi import FastAPI, File, UploadFile, HTTPException
import openai
import tempfile
import os

app = FastAPI()

# Set up OpenAI API key (store in .env)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # Save Uploaded file to temp location
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error reading file: {str(e)}")

    suffix = "." + file.filename.split(".")[-1] if "." in file.filename else ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving tempory file: {str(e)}")

    try:
        result = {"message": "Processing Complete"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return result
