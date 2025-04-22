import pandas as pd
import requests
import os
import json
from tqdm import tqdm
from typing import Tuple

from concurrent.futures import ThreadPoolExecutor, as_completed

def transcribe_audio(api_url: str, audio_file_path: str) -> Tuple[str, str]:

    """
    Transcribes a single audio file

    Args:
        api_url (str):         The URL of the API to send the request
        audio_file_path (str): The path to the audio file

    Returns:
        str: The transcription of the audio file
    """

    # Parse the audio file into binary data
    with open(audio_file_path, 'rb') as audio_f:

        # Send the POST request
        response = requests.post(api_url, files={"file": audio_f})

        # Parse the API result to retrieve the transcription and duration
        result = json.loads(response.text)
        transcription = result['transcription']
        duration = result['duration']

        return (transcription, duration)
    
if __name__ == "__main__":

    API_URL = "http://localhost:8001/asr"
    BASE_DIR = "common_voice/cv-valid-dev"
    OUTPUT_FILENAME = "cv-valid-dev-v2.csv"

    # Read the CSV dataset into a Pandas Dataframe
    cv_dev_df = pd.read_csv("common_voice/cv-valid-dev.csv")

    with tqdm(total=len(cv_dev_df)) as progress_bar: # Progress bar

        transcriptions = {}
        durations = {}

        # Set up ThreadPoolExecutor to perform concurrent API calls, with the max number of workers set to the machine's CPU count
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor: 

            futures = {}

            # Iterate over the rows in the dataframe
            for _, row in cv_dev_df.iterrows():

                full_audio_file_dir = os.path.join(BASE_DIR, row['filename'])

                # Submit job
                curr_future = executor.submit(transcribe_audio, API_URL, full_audio_file_dir)
                futures[curr_future] = row['filename']

            for future in as_completed(futures):

                # Get filename
                filename = futures[future]

                # Save transcription
                transcriptions[filename] = future.result()

                progress_bar.update(1)

        # Append transcriptions and durations to new column in the dataframe, using filename for mapping
        cv_dev_df[['generated_text', 'duration']] = cv_dev_df['filename'].map(transcriptions) \
                                                                         .apply(pd.Series)

        # Save the new dataframe to a .csv file
        cv_dev_df.to_csv(OUTPUT_FILENAME, index=False)

                








