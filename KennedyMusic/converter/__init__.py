from os import listdir, mkdir

if "raw_files" not in listdir():
    mkdir("raw_files")

from KennedyMusic.converter.converter import convert

__all__ = ["convert"]
