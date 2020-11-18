from tqdm import tqdm
from multiprocessing import Pool
import ffmpeg
import numpy as np
import glob, sys
import librosa

from utils import *
import configs as cfg

NUM_JOBS = cfg.num_jobs


class Video2Wav_Converter():
	def __init__(self, input_video_dataset_path, extracted_wav_savepath, input_file_format='mp4', acodec='pcm_s16le', sampling_rate='22050'):
		input_video_dataset_path = get_path(input_video_dataset_path, "*.{}".format(input_file_format))
		self.video_file_list = glob.glob(input_video_dataset_path)
		self.acodec, self.sampling_rate = acodec, sampling_rate
		self.extracted_wav_savepath = extracted_wav_savepath


	def job(self, video_filename):
		video_file_format = video_filename.split(".")[-1]
		extracted_wav_filename = get_path(self.extracted_wav_savepath, video_filename.split("/")[-1].replace(video_file_format, "wav"))

		self.__extract_wav_from_video(in_filename=video_filename, out_filename=extracted_wav_filename, acodec=self.acodec, sampling_rate=self.sampling_rate)		# convert video2wav 
		self.__remove_background_music(in_filename = extracted_wav_filename, out_filepath=self.extracted_wav_savepath)											# remove background noise


	def do(self):
		print("\n[LOG] Start Video2Wav Converter...")
		p = Pool(NUM_JOBS)
		with tqdm(total=len(self.video_file_list)) as pbar:
			for _ in tqdm(p.imap_unordered(self.job, self.video_file_list)):
            			pbar.update()	
		print("\n[LOG] Finish converting!")

	def __extract_wav_from_video(self, in_filename, out_filename, acodec, sampling_rate):

		try:
			out, err = (ffmpeg
					.input(in_filename)
					.output(out_filename, acodec=acodec, ac=1, ar=sampling_rate)
					.overwrite_output()
					.run(capture_stdout=True, capture_stderr=True))

		except ffmpeg.Error as err:
			print(err.stderr, file=sys.stderr)
			raise

	def __remove_background_music(self, in_filename, out_filepath):
		os.system("spleeter separate -i {} -o {}".format(in_filename, out_filepath))
	





