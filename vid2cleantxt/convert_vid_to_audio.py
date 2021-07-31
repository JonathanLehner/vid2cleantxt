"""
This script takes the input folder, searches through the whole folder for videos (including all subdirectories)
and converts them to audio files stored in a folder created in the initially input path.
"""
import os
import pprint as pp
from moviepy.editor import *
from natsort import natsorted
from os.path import basename, join
from tqdm.auto import tqdm


def load_dir_files(directory, req_extension=".txt", return_type="list",
                   verbose=False):
    appr_files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(directory):
        for prefile in f:
            if prefile.endswith(req_extension):
                fullpath = os.path.join(r, prefile)
                appr_files.append(fullpath)

    appr_files = natsorted(appr_files)

    if verbose:
        print("A list of files in the {} directory are: \n".format(directory))
        if len(appr_files) < 10:
            pp.pprint(appr_files)
        else:
            pp.pprint(appr_files[:10])
            print("\n and more. There are a total of {} files\n\n".format(len(appr_files)))

    if return_type.lower() == "list":
        return appr_files
    else:
        if verbose: print("returning dictionary")

        appr_file_dict = {}
        for this_file in appr_files:
            appr_file_dict[basename(this_file)] = this_file

        return appr_file_dict


def create_folder(filepath):
    os.makedirs(filepath, exist_ok=True)


dirpath = str(input("please enter path to folder containing videos -->"))
audio_folder = join(dirpath, "audio_only")
create_folder(audio_folder)
this_ext = ".mp4"
vidfiles = load_dir_files(dirpath, req_extension=this_ext, verbose=True)

for vidfile in tqdm(vidfiles, total=len(vidfiles), desc="converting to mp3"):
    # establish filenames etc
    this_name = basename(vidfile)
    audio_name = this_name.replace(this_ext, ".mp3")
    save_path = join(audio_folder, audio_name)
    # read and write
    audioclip = AudioFileClip(vidfile)
    audioclip.write_audiofile(save_path)

print("finished, files are in here: \n{}".format(dirpath))
