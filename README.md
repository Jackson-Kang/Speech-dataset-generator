# Speech-dataset-generator
Simple implementation of speech dataset generator for deep-learning based ASR and TTS

# Introduction
These days, deep-learning-based ASR and TTS are getting popular. Despite of its success, training deep-learning based ASR and TTS models requires huge amount of data. Therefore, it is mendatory to collect data automatically from various web services. 

In a response to that necessity, I made a program, which generates speech dataset (i.e., text-wav pair). This program supports following functions:
* Extract wav signals from video (currently, only supports mp4-formatted video files), while removing background noise such as music, sound effects and etc..
* Segment one long wav-signal into multiple segments, removing silence.
* Transcribe segmented wav-signal using [Google Speech-to-Text(STT) api](https://cloud.google.com/speech-to-text)

**Please note that generated dataset cannot be good. Also, this project was tested on Korean, so not sure that it works on other languages.**

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

# Notes
* To remove various kind of noises such as music, sound effects and etc, I used [spleeter](https://github.com/deezer/spleeter), which is originally used to source separation task.
* Google ASR system seems to produce various error such as CER and WER from noisy segmented speech, but it reasonably works on clean speech dataset.

# Acknowledgements
This project is based on following works:
* Spleeter [R. Hennequin et. al., 2019] ( [paper](http://archives.ismir.net/ismir2019/latebreaking/000036.pdf) [github](https://github.com/deezer/spleeter) )
* [Google STT api](https://cloud.google.com/speech-to-text/?hl=ko&utm_source=google&utm_medium=cpc&utm_campaign=japac-KR-all-ko-dr-bkws-all-all-trial-e-dr-1009137&utm_content=text-ad-none-none-DEV_c-CRE_288266945691-ADGP_Hybrid%20%7C%20AW%20SEM%20%7C%20BKWS%20~%20T1%20%7C%20EXA%20%7C%20ML%20%7C%20M%3A1%20%7C%20KR%20%7C%20ko%20%7C%20Speech%20%7C%20Text%20%7C%20en-KWID_43700035804893418-kwd-21425535976&userloc_1009864-network_g&utm_term=KW_google%20speech%20to%20text&gclid=CjwKCAiAzNj9BRBDEiwAPsL0d7Z59YCBOU04wMpKoERxAjP7xlK6t6abI40496bgWRKEghlI_bdzrhoC_LkQAvD_BwE)
