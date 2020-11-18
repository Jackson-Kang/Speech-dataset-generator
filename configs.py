from utils import get_path

# step 1: options for video2wav.py
input_video_data_path = "/home/minsu/hdd/dataset/videos/"
preprocessed_wav_savepath = "preprocessed_wavs"
extracted_wav_savepath = get_path(preprocessed_wav_savepath, "unsegmented_wavs")

# step 2: segment
input_wav_path = extracted_wav_savepath
segmented_wav_path = get_path(preprocessed_wav_savepath, "segmented_wavs")

num_jobs = 4



# audio info
input_video_format = "mp4"
acodec = 'pcm_s16le'
audio_sampling_rate = 22050
