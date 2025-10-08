from moviepy import VideoFileClip
import os


class VideoConfig:

    def __init__(self, path = "", fps = 15, resolution = 480, is_length_chosen = False, start = 0, end = 10, is_destination_chosen = False, destination = ""):
        self.fps = fps
        self.resolution = resolution
        self.is_length_chosen = is_length_chosen
        self.path = path
        self.start = start
        self.end = end
        self.is_destination_chosen = is_destination_chosen
        self.destination = destination

    def __eq__(self, other):
        if isinstance(other, VideoConfig):
            return self.path == other.path
        if isinstance(other, str):
            return self.path == other

    def __repr__(self):
        return self.path
def convert_videos_to_gifs(videos: list[VideoConfig]) -> None:

    for video in videos:

        clip = VideoFileClip(video.path)

        clip = clip.subclipped(video.start, video.end)
        clip = clip.resized(height = video.resolution)

        file_name = os.path.basename(video.path)
        name_without_extension = os.path.splitext(file_name)[0]

        name = name_without_extension

        if video.is_destination_chosen:
            name = os.path.join(video.destination, name)

        clip.write_gif(name + ".gif", fps = video.fps)