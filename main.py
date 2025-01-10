from fastapi import FastAPI, File, UploadFile, HTTPException
import openai
import tempfile
import os

app = FastAPI()

# Set up OpenAI API key (store in .env)
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe_audio_file(file_path: str) -> str:
    """Helper function, transcribes the audio file using whispers API."""
    with open(file_path, 'r') as audio_file:
        transcribe_results = openai.Audio.transcribe("whisper-1", audio_file)
    return transcribe_results.get("text", "")


def summarize_text(transcript: str) -> str:
    """Helper function which Summarizes the transcript using ChatGBT"""
    summary_prompt = f"summarize the following transcript:/n/n{transcript}"
    completion = openai.ChatCompletion.create(
        model="gbt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that sumarizes audio transrciptions."},
            {"role": "user", "content": summary_prompt}
        ],
        temperature=0.5,
    )
    return completion.choice[0].message["content"]


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint to transcribe an uploaded audio file and summarize its content.

    This function:
    1. Accepts an uploaded audio file.
    2. Saves the file temporarily.
    3. Uses OpenAI's Whisper API to transcribe the audio.
    4. Summarizes the transcription using ChatGPT.
    5. Returns a JSON response with the full transcript and summary.

    Args:
        file (UploadFile): The audio file uploaded by the user.

    Returns:
        dict: A dictionary containing the transcript and summary. Example:
            {
                "transcript": "Full transcription text...",
                "summary": "Summarized version of the transcript..."
            }

    Raises:
        HTTPException: If there's an error reading the file, saving the
                       temporary file, or during processing the
                       transcription/summarization.
    """
    try:
        contents = await file.read()
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
            status_code=500, detail=f"Error saving temporary file: {str(e)}")

    try:
        transcript = transcribe_audio_file(tmp_path)
        summary = summarize_text(transcript)
        result = {"transcript": transcript, "summary": summary}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
