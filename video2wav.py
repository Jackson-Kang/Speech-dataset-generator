from tqdm import tqdm
from multiprocessing import Pool
import ffmpeg
import numpy as np
import glob, sys
import librosa

from utils import *
import configs

NUM_JOBS = configs.num_jobs


class Video2Wav_Converter():
	def __init__(self, video_dataset_path, input_file_format='mp4', acodec='pcm_s16le', sampling_rate='22050'):
		video_dataset_path = get_path(video_dataset_path, "*.{}".format(input_file_format))
		self.video_file_list = glob.glob(video_dataset_path)
		self.acodec, self.sampling_rate = acodec, sampling_rate

		self.preprocessed_wav_savepath = "./preprocessed_wavs"
		create_dir(self.preprocessed_wav_savepath)


	def job(self, fpath):
		audio_filename = self.__extract_wav_from_video(in_filename=fpath, acodec=self.acodec, sampling_rate=self.sampling_rate)		# convert video2wav 
		self.__remove_background_music(audio_filename)											# remove background noise


	def do(self):
		print("\n[LOG] Start Video2Wav Converter...")
		p = Pool(NUM_JOBS)
		with tqdm(total=len(self.video_file_list)) as pbar:
			for _ in tqdm(p.imap_unordered(self.job, self.video_file_list)):
            			pbar.update()	
		print("\n[LOG] Finish converting!")

	def __extract_wav_from_video(self, in_filename, acodec, sampling_rate):

		file_format = in_filename.split(".")[-1]
		out_filename = in_filename.replace(file_format, "wav")

		try:
			out, err = (ffmpeg
					.input(in_filename)
					.output(out_filename, acodec=acodec, ac=1, ar=sampling_rate)
					.overwrite_output()
					.run(capture_stdout=True, capture_stderr=True))

		except ffmpeg.Error as err:
			print(err.stderr, file=sys.stderr)
			raise
        
		return out_filename

	def __remove_background_music(self, input_filename):
		os.system("spleeter separate -i {} -o {}".format(input_filename, self.preprocessed_wav_savepath))
	





