import sys
import configs as cfg
from video2wav import Video2Wav_Converter

def convert_video_to_wav():
	v2w = Video2Wav_Converter(video_dataset_path=cfg.video_data_path, input_file_format=cfg.input_video_format, acodec=cfg.acodec, sampling_rate=cfg.audio_sampling_rate)
	v2w.do()



def segment_wav():
	print("done")





if __name__ == "__main__":

	assert len(sys.argv) == 3, "[ERROR] option must be provided!"

	if sys.argv[1].lower() in ["True", "1"]:
		convert_video_to_wav()

	if sys.argv[2].lower() in ["True", "1"]:
		segment_wav()
