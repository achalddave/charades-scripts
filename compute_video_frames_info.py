"""Output frames per second, number of frames for each video.

Output is a CSV file containing the entries
video,fps,num_frames

where video is the name of the video file without the extension.
"""

import argparse
import csv
import os

from moviepy.editor import VideoFileClip
from tqdm import tqdm


def main(video_paths_list, output_csv_path):
    with open(video_paths_list) as f:
        video_paths = [line.strip() for line in f]

    with open(output_csv_path, 'w') as output:
        field_names = ['video', 'fps', 'num_frames']
        writer = csv.DictWriter(output, fieldnames=field_names)
        writer.writeheader()
        for video_path in tqdm(video_paths):
            clip = VideoFileClip(video_path)
            frames_per_second = clip.fps
            num_frames = int(clip.fps * clip.duration)
            file_basename = os.path.splitext(os.path.basename(video_path))[0]
            writer.writerow({'video': file_basename,
                            'fps': frames_per_second,
                            'num_frames': num_frames})


if __name__ == "__main__":
    # Use first line of file docstring as description if a file docstring
    # exists.
    parser = argparse.ArgumentParser(
        description=__doc__.split('\n')[0] if __doc__ else '',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'video_list',
        help='File containing new-line separated paths to videos.')
    parser.add_argument('output_csv')
    args = parser.parse_args()

    main(args.video_list, args.output_csv)
