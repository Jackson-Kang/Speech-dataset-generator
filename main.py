import sys
import configs as cfg

from video2wav import Video2Wav_Converter
from segment_and_transcribe_speech import Segment_Speech, Transcribe_Speech
from utils import create_dir

def convert_video_to_wav():

	create_dir(cfg.preprocessed_wav_savepath)
	create_dir(cfg.extracted_wav_savepath)

	v2w = Video2Wav_Converter(input_video_dataset_path=cfg.input_video_data_path, 
				  input_file_format=cfg.input_video_format, 
				  extracted_wav_savepath=cfg.extracted_wav_savepath,
				  acodec=cfg.acodec, 
				  sampling_rate=cfg.audio_sampling_rate)
	v2w.do()



def segment_and_transcribe_speech():

	create_dir(cfg.preprocessed_wav_savepath)
	create_dir(cfg.segmented_wav_path)

	ss, ts = Segment_Speech(), Transcribe_Speech()
	ss.do()
	ts.do()


if __name__ == "__main__":

	assert len(sys.argv) == 3, "[ERROR] option must be provided!"

	if sys.argv[1].lower() in ["True", "1"]:
		convert_video_to_wav()

	if sys.argv[2].lower() in ["True", "1"]:
		segment_speech()
