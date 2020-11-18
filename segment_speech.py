from multiprocessing import Pool
from pydub import AudioSegment, silence
from utils import get_path, create_dir, write_meta
from tqdm import tqdm

import configs as cfg
import glob

NUM_JOBS = cfg.num_jobs

class Segment_Speech():
	def __init__(self, in_unsegmented_wav_path, out_wav_savepath, input_file_format="wav", sampling_rate="22050", silence_thresh=-40, min_silence_len=400, silence_chunk_len=100, keep_silence=100, skip_idx=0):
		
		wav_path = get_path(in_unsegmented_wav_path, "**/vocals.{}".format(input_file_format))
		self.wav_file_list = glob.glob(wav_path, recursive=True)
		self.out_wav_savepath = out_wav_savepath

		self.silence_chunk_len, self.silence_thresh, self.min_silence_len, self.keep_silence, self.skip_idx = silence_chunk_len, silence_thresh, min_silence_len, keep_silence, skip_idx

	def job(self, in_wav_filename):

		out_wav_filepath = create_dir(self.out_wav_savepath, in_wav_filename.split("/")[-2])
		self.__segment_speech(in_wav_filename, out_wav_filepath, self.silence_chunk_len, self.silence_thresh, self.min_silence_len, self.keep_silence, self.skip_idx)


	def do(self):
		print("\n[LOG] Start Segment Speech...")
		p = Pool(NUM_JOBS)
		with tqdm(total=len(self.wav_file_list)) as pbar:
			for _ in tqdm(p.imap_unordered(self.job, self.wav_file_list)):
				pbar.update()
		print("\n[LOG] Finish segmenting!")


	def __segment_speech(self, in_wav_filename, out_wav_filepath,  silence_chunk_len, silence_thresh, min_silence_len, keep_silence, skip_idx):
		audio = AudioSegment.from_file(in_wav_filename)
		not_silence_ranges = silence.detect_nonsilent(audio,
							      min_silence_len=silence_chunk_len, 
							      silence_thresh=silence_thresh)
		edges = [not_silence_ranges[0]]
		audio_paths = []

		for idx in range(1, len(not_silence_ranges)-1):
			cur_start = not_silence_ranges[idx][0]
			prev_end = edges[-1][1]

			if cur_start - prev_end < min_silence_len:
				edges[-1][1] = not_silence_ranges[idx][1]
			else:
				edges.append(not_silence_ranges[idx])

		for idx, (start_idx, end_idx) in enumerate(edges[skip_idx:]):
			start_idx = max(0, start_idx - keep_silence)
			end_idx += keep_silence
			target_audio_path = "{}/{:04d}.wav".format(out_wav_filepath, idx)
			segment = audio[start_idx: end_idx]
			segment.export(target_audio_path, "wav")
			audio_paths.append(target_audio_path)

		return audio_paths
