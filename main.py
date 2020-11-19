import sys
import configs as cfg

from video2wav import Video2Wav_Converter
from segment_speech import Segment_Speech
from transcribe_speech import Transcribe_Speech

from utils import create_dir


def convert_video_to_wav():

	create_dir(cfg.preprocessed_wav_savepath)
	create_dir(cfg.extracted_wav_savepath)

	v2w = Video2Wav_Converter(input_video_dataset_path=cfg.input_video_data_path, 
				  input_file_format=cfg.input_video_format, 
				  extracted_wav_savepath=cfg.extracted_wav_savepath,
				  acodec=cfg.acodec, 
				  sampling_rate=cfg.wav_extraction_output_sampling_rate)
	v2w.do()



def segment_speech():

	create_dir(cfg.preprocessed_wav_savepath)
	create_dir(cfg.segmented_wav_savepath)

	ss = Segment_Speech(in_unsegmented_wav_path=cfg.unsegmented_input_wav_path,
			    out_wav_savepath = cfg.segmented_wav_savepath,
			    input_file_format = cfg.segmentation_input_wav_format,
			    sampling_rate = cfg.segmentation_source_sampling_rate,
			    resampling_rate = cfg.segmentation_output_resampling_rate,
			    min_silence_len=400,
			    keep_silence=100,
			    silence_chunk_len=100,
			    silence_thresh=-40, 
			    skip_idx=0)
	ss.do()


def transcribe_speech():

	ts = Transcribe_Speech(in_segmented_wav_path = cfg.segmented_input_wav_path,
			       out_meta_filename = cfg.meta_name,
			       input_file_format = cfg.transcription_input_wav_format,
			       sampling_rate = cfg.transcription_audio_sampling_rate,
			       wav_channel = cfg.wav_channel,
			       language_code=cfg.language_code)
	ts.do()


if __name__ == "__main__":

	assert len(sys.argv) == 2, "[ERROR] option must be provided!"

	if sys.argv[1] in [0, "0"]:
		convert_video_to_wav()

	elif sys.argv[1] in [1, "1"]:
		segment_speech()
	elif sys.argv[1] in [2, "2"]:
		transcribe_speech()
