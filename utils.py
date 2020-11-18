import os

def get_path(*args):
        return os.path.join('', *args)

def create_dir(*args):
        path = get_path(*args)
        if not os.path.exists(path):
                os.mkdir(path)
        return path


def write_meta(out_filename, transcript):
	with open(out_filename, "w") as f:
		f.write(transcript)
