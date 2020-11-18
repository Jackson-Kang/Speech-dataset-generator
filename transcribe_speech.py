from multiprocessing import Pool
from utils import get_path, create_dir, write_meta
from tqdm import tqdm

from google.cloud import speech

import configs as cfg
import glob, io, os


import numpy as np



NUM_JOBS = cfg.num_jobs

class Transcribe_Speech():
	def __init__(self, in_segmented_wav_path, out_meta_filename, input_file_format, sampling_rate="22050", language_code="ko-KR"):

		wav_path = get_path(in_segmented_wav_path, "**/*.{}".format(input_file_format))
		self.wav_file_list = glob.glob(wav_path, recursive=True)
		self.input_file_format = input_file_format
		self.meta_filename = out_meta_filename

		self.client = speech.SpeechClient()
		self.recognition_config = speech.RecognitionConfig(
					encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
					audio_channel_count=2,
					enable_separate_recognition_per_channel=True,
					sample_rate_hertz= int(sampling_rate),
					language_code=language_code)				 
 

	def job(self, in_wav_filename):
		out_txt_filename = in_wav_filename.split(".")[0] + ".txt"
		self.__recognize_text(in_wav_filename, out_txt_filename, recognition_config=self.recognition_config)		

	def do(self):
		print("\n[LOG] Start Transcribe Speech...")
		#p = Pool(NUM_JOBS)
		#with tqdm(total=len(self.wav_file_list)) as pbar:
		#	for _ in tqdm(p.imap_unordered(self.job, self.wav_file_list)):
		#		pbar.update()	

		for in_wav_filename in self.wav_file_list:
			self.job(in_wav_filename)

		self.__combine_transcript_and_write_meta()
		print("\n[LOG] Finish transcription!")

	def __recognize_text(self, in_wav_filename, out_txt_filename, recognition_config):
		if os.path.exists(out_txt_filename):
			return

		out, error_count, transcript = {}, 0, ""
		while True:
			try:
				with io.open(in_wav_filename, 'rb') as f:
					audio = speech.RecognitionAudio(content=f.read())
				response = self.client.recognize(request = {"config": recognition_config, "audio": audio})

				if len(response.results) >0:
					alternatives = response.results[0].alternatives

					results = [alternative.transcript for alternative in alternatives]

					assert len(results) == 1, "More than 1 results: {}".format(results)
					transcript = "" if len (results) == 0 else results[0]

					break
				else:
					transcript = ""
				break

			except Exception as err:
				raise Exception("OS error: {0}".format(err))
				error_count+=1
				
				print("Skip warning for {} for {} times".format(out.filename.split("/")[-1], error_count))
				if error_count > 3:
					break
				else:
					continue
		if transcript != "":
			write_meta(out_txt_filename, transcript)

	def __combine_transcript_and_write_meta(self):
		print("Done!!!!!!!!")
