import torch
import torchaudio
from torchaudio.transforms import Resample
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
from io import BytesIO

app = FastAPI()

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# Ping API (for testing)
@app.get("/ping")
async def ping():
    return JSONResponse(
        status_code=200,
        content="pong"
    )

@app.post("/asr")
async def asr(file: UploadFile = File(...)) -> Dict[str, str]:

    """
    Performs transcription of an MP3 audio file

    Args:
        file (str): the binary of an audio MP3 file

    Returns:
        dict:
            A dictionary containing:
            - transcription (str): the transcribed text returned by the model
            - duration (str): the duration of the file in seconds 
    """
    SAMPLE_RATE = 16000 # Expected sample rate

    # Read file contents
    contents = await file.read()
    
    # Check if file is empty
    if not contents:
        raise HTTPException(status_code=400, detail="The specified audio file is empty.")

    try:
        waveform, sample_rate = torchaudio.load(BytesIO(contents))

        if sample_rate != SAMPLE_RATE:
            resampler = Resample(sample_rate, SAMPLE_RATE, dtype=waveform.dtype)
            waveform = resampler(waveform)
    except:
        raise HTTPException(status_code=400, detail="Unable to load audio data. Please ensure the audio file is valid / not corrupted.")

    input_values = processor(waveform[0], return_tensors="pt", padding="longest").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]

    # Retrieve the metadata of the audio file
    audio_metadata = torchaudio.info(BytesIO(contents))

    # Calculate the duration of the audio file (Number of frames / Sample rate)
    audio_duration = round(audio_metadata.num_frames / audio_metadata.sample_rate, 1)

    return JSONResponse(
        status_code=200,
        content={"transcription": transcription, "duration": str(audio_duration)}
    )
