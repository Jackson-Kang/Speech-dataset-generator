# Speech-dataset-generator
Simple implementation of speech dataset generator for deep-learning based ASR and TTS

# Introduction
These days, deep-learning-based ASR and TTS are getting popular. Despite of its success, training deep-learning based ASR and TTS models requires huge amount of data. Therefore, it is mendatory to collect data automatically from various web services. 

In a response to that necessity, I made a program, which generates speech dataset (i.e., text-wav pair). This program supports following functions:
* Extract wav signals from video (now, only supports mp4-formatted video files), while removing background noise such as music, sound effects and etc..
* Segment one long wav-signal into multiple segments, removing silence.
* Transcribe segmented wav-signal using [Google Speech-to-Text(STT) api](https://cloud.google.com/speech-to-text)

**Please note that this project was made using various deep-learning based signal processing module, so generated dataset are not good. Also, this project was tested on Korean, so not sure that it works on other languages.**

# How-to-use
## 1. Install dependencies
python=3.7 and anaconda env. is strongly recommended.
1. First, install ffmpeg via following command:
```
sudo apt-get install ffmpeg
```
2. Next, install python dependencies
```
pip install -r requirements.txt
```
## 2. Prepare credentials for Google STT API
Please visit [this site](https://cloud.google.com/docs/authentication/production) to get "<your-key.json>". After that, edit first line of "run.sh", so that environment variable "GOOGLE_APPLICATION_CREDENTIALS" can point  your "<your-key.json>" file. 
For example,
```
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Speech-dataset-generator/google_api_credentials/<your-key.json>"
```

## 3. Generate speech dataset
Please set hyperparameter in "configs.py" and make sure that "<input_video_data_path>" variable is correctly point "<your-path-to-video-dataset>". After that, you can run this program via a shell script, "run.sh" file. In the project repository, just simply type following command:
```
bash run.sh
```
