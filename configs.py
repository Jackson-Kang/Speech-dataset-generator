from utils import get_path


# step 1: options for video2wav.py
input_video_data_path = "/home/minsu/hdd/dataset/videos/"
preprocessed_wav_savepath = "preprocessed_wavs"
extracted_wav_savepath = get_path(preprocessed_wav_savepath, "unsegmented_wavs")

wav_extraction_output_sampling_rate = 44100
input_video_format = "mp4"
acodec = "pcm_s16le"


# step 2: segment speech
unsegmented_input_wav_path = extracted_wav_savepath
segmented_wav_savepath = get_path(preprocessed_wav_savepath, "segmented_wavs")

segmentation_source_sampling_rate = wav_extraction_output_sampling_rate
segmentation_output_resampling_rate = 22050
segmentation_input_wav_format = "wav"


#step 3: transcribe speech
segmented_input_wav_path = segmented_wav_savepath
meta_name = get_path(segmented_input_wav_path, "metadata.csv")

transcription_audio_sampling_rate = 22050
wav_channel = 2				# (mono): 1 or (stereo) : 2
transcription_input_wav_format = "wav"

language_code = "ko-KR"


# hardware option
num_jobs = 8
