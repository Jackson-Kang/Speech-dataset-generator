export GOOGLE_APPLICATION_CREDENTIALS="/home/minsu/hdd/Speech-dataset-generator/google_api_credentials/smilegate20-data-generator-3aa2df790228.json"


# Step 1: video2wav
python main.py 0

# Step 2: Speech segmentation
python main.py 1

# Step 3: Speech Transcription
python main.py 2
