'''
    Attempts to test a file for specific
    attributes
'''

import os
import re
from PIL import Image


def detect_special_characters(file_name):
    '''
        Attempts to detect whether a filename contains
        special characters. Special characters are bad

        We only accept the following characters:
        a-z
        a-Z
        _ (underscores)
        0-9

        Anything else should not be allowed.

        return: None || dict
    '''
    pattern = "^[a-zA-Z0-9_]*\.(mov|dv|mp4)"
    if re.match(pattern, file_name):
        return None
    else:
        return {'special_chars': 'The file contains bad characters, only A-Z, 0-9, and underscores.'}

def detect_whitespace(file_name):
    '''
        Attempts to detect whether whitespaces exist in a give file name.

        file_name: name of file

        return: None || dict
    '''
    if ' ' in file_name:
        return {"whitespace": 'File name contains whitespaces.'}
    return None


def detect_thumbnails(thumbnail_path):
    '''
        Attempts to detect whether a thumbnail exists for a given asset.
        All video assets should also have a thumbnail.

        thumbnail_path: path of the thumbnail

        return: None || dict
    '''
    if os.path.exists(thumbnail_path):
        return None
    return {"thumbs": "Thumbnail is missing"}


def detect_thumbnail_size(thumbnail_path, quality):
    '''
        Attempts check the thumbnail sizes. Each thumbnail should less than 500px x 500px

        thumbnail_path: path of the thumbnail

        return: None || dict
    '''
    img = Image.open(thumbnail_path)
    width, height = img.size
    if width > 500 or height > 500:
        return {'thumb_size': "Thumbnail sizes are incorrect, found: %s x %s " % (width, height)}
    return None


def detect_video_type(file_name):
    '''
        Attempts to check a file and determines the video type.
        Possible video types: Scene, Clip, Unknown

        Unknown is bad!

        file_name: name of file to check

        return: Unknown || Scene || Clip
    '''
    # If neither regex catches, send back 'Unknown'
    media = "Unknown"
    # Test to see if the file is a scene
    if re.match('^([0-9]+)_s([0-9]+|[wWxXyYzZ][wWxXyYzZ])_.*.(dv|hdv|mov|mp4|mxf|mpeg)$', file_name):
        media = "Scene"
    # Test to see if file is a clip/promo
    if re.match('^([0-9]+)_([0-9]|pos|pre_promo|pre_scene)*.(dv|hdv|mov|mp4|mxf|mpeg)$', file_name):
        media = "Clip"
    return media


def detect_file_name_matches(id, file_name):
    '''
        Attempts to make sure that the name of the video file also contains
        the id in this format:
        <ID>_.<EXT>

        id: id
        file_name: file name of video

        return: None || dict
    '''
    # cast id to string to avoid truthyness failures
    id = str(id)
    if file_name.split('_')[0] != id:
        return {'id': 'Either the Id does not match or the file is misnamed.'}
    return None

def tests(id, file_path, quality):
    '''
        Attempts to runs through a series of test for a given file

        id: id
        file_path: path of asset

        return: a list with error message
    '''
    error_list = []

    # export_path will be /media/fauxarchive/incoming/31726/exports
    export_path, video_file = os.path.split(file_path)
    # This should be /media/fauxarchive/incoming/31726
    # Attempt to get the basename of the video file (same as thumbnail)
    # thumbnail_name = 12345_7
    thumbnail_name, ext = os.path.splitext(video_file)
    thumbnail_file_path = os.path.join(os.path.join(os.path.split(export_path)[0], "thumbs"), thumbnail_name + ".jpg")

    # Test for special characters
    error_list.append(detect_special_characters(video_file))

    # Test for whitespace in the file name
    error_list.append(detect_whitespace(video_file))

    # Check that filename begins with id
    error_list.append(detect_file_name_matches(id, video_file))

    # Test video type
    # we only want 'Clip' or 'Scene'
    if detect_video_type(video_file) is 'Unknown':
        error_list.append({"file_name": "File name is miss-named"})

    # Test of existance of thumbnails
    thumbnail_exist_results = detect_thumbnails(thumbnail_file_path)
    if thumbnail_exist_results:
        error_list.append(thumbnail_exist_results)
    else:
        # If thumbnails exist, test their sizes
        error_list.append(detect_thumbnail_size(thumbnail_file_path, quality))

    # Remove the None entries because we're only interested in failures
    error_list = filter(None, error_list)
    return error_list
