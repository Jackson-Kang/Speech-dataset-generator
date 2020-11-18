export GOOGLE_APPLICATION_CREDENTIALS="YOUR-GOOGLE.CREDENTIALS.json"


# Step 1: video2wav
python main.py 0

# Step 2: Speech segmentation
python main.py 1

# Step 3: Speech Transcription
python main.py 2
