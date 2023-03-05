from django.core.files import File

from pydub import AudioSegment
from pathlib import Path

import os


def convert_to_mp3(temp_file, file_extension='mp3', content_type='audio/mpeg', bitrate='192k'):
    temp_file_path = temp_file.temporary_file_path()
    print(temp_file_path)
    audiofile = AudioSegment.from_wav(temp_file_path)

    new_path = temp_file_path[:-3] + file_extension
    print(new_path)
    audiofile.export(new_path, format=file_extension, bitrate=bitrate)

    converted_audiofile = File(file=open(new_path, 'rb'), name=Path(new_path))
    converted_audiofile.name = Path(new_path).name
    converted_audiofile.content_type = content_type
    converted_audiofile.size = os.path.getsize(new_path)

    return converted_audiofile
