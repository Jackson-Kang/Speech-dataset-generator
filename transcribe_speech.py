from multiprocessing import Pool
from utils import get_path, create_dir, write_meta, read_meta
from tqdm import tqdm

from google.cloud import speech
from pydub.utils import mediainfo

import configs as cfg
import glob, io, os
import numpy as np



NUM_JOBS = cfg.num_jobs

class Transcribe_Speech():
	def __init__(self, in_segmented_wav_path, out_meta_filename, input_file_format, sampling_rate="22050", wav_channel=2, language_code="ko-KR"):

		wav_path = get_path(in_segmented_wav_path, "**/*.{}".format(input_file_format))
		self.in_segmented_wav_path = in_segmented_wav_path
		self.wav_file_list = glob.glob(wav_path, recursive=True)
		self.input_file_format = input_file_format
		self.meta_filename = out_meta_filename

		self.client = speech.SpeechClient()

		self.language_code = language_code
		self.sampling_rate=sampling_rate
		self.wav_channel = wav_channel

	def job(self, in_wav_filename):
		out_txt_filename = in_wav_filename.split(".")[0] + ".txt"
		self.__recognize_text(in_wav_filename, out_txt_filename, sampling_rate=self.sampling_rate, wav_channel=self.wav_channel, language_code=self.language_code)		

	def do(self):
		print("\n[LOG] Start Transcribe Speech...")
		#p = Pool(NUM_JOBS)
		#with tqdm(total=len(self.wav_file_list)) as pbar:
		#	for _ in tqdm(p.imap_unordered(self.job, self.wav_file_list)):
		#		pbar.update()	

		for in_wav_filename in tqdm(self.wav_file_list):
			self.job(in_wav_filename)

		self.__combine_transcript_and_write_meta(in_segmented_wav_path=self.in_segmented_wav_path, out_meta_filename = self.meta_filename)
		print("\n[LOG] Finish transcription!")

	def __recognize_text(self, in_wav_filename, out_txt_filename, sampling_rate=22050, wav_channel=2, language_code='ko-KR'):
		if os.path.exists(out_txt_filename):
			return

		out, error_count, transcript = {}, 0, ""

		with io.open(in_wav_filename, 'rb') as f:
			audio = f.read()

		duration = mediainfo(in_wav_filename)['duration']
		enable_separate_recognition_per_channel = False if wav_channel ==1 else True

		recognition_config = speech.RecognitionConfig(
					encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
					audio_channel_count=wav_channel,
					enable_separate_recognition_per_channel=enable_separate_recognition_per_channel,
					sample_rate_hertz= int(sampling_rate),
					language_code=language_code)				 

		audio_object = speech.RecognitionAudio(content=audio)

		while True:
			try:
				response = self.client.recognize(request = {"config": recognition_config, "audio": audio_object})

				if len(response.results) >0:
					alternatives = response.results[0].alternatives

					results = [alternative.transcript for alternative in alternatives]

					assert len(results) == 1, "More than 1 results: {}".format(results)
					transcript = "" if len (results) == 0 else "{}|{}|{}".format(in_wav_filename.split("/")[-1], results[0], duration)

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

	def __combine_transcript_and_write_meta(self, in_segmented_wav_path, out_meta_filename):
		in_txt_path_list = glob.glob(get_path(in_segmented_wav_path, "**/*.txt"))
		contents = ""
		for _, in_txt_path in enumerate(in_txt_path_list):
			content = read_meta(in_txt_path)[0].rstrip() + "\n"
			if content != "":
				contents += content

		write_meta(out_meta_filename, contents)

