"""Parse temporal annotations for the Charades data, output JSON.

Output format:
    [
        {
            filename: ...,
            subject: ...,
            verified: ...,
            quality: ...,
            start_seconds: ...,
            end_seconds: ...,
            start_frame: ...,
            end_frame: ...,
            frames_per_second: ...,
            category: ...
        },
        ...
    ]
"""

import argparse
import csv
import json
import os
import re
from math import ceil, floor
from os import path


def main(input_annotations_path, charades_classes_path, video_frames_info_path,
         output):
    class_mapping = {}
    with open(charades_classes_path) as f:
        # Lines are of the form '<class_id> <class_description>'
        class_matcher = re.compile('([^\s]*) (.*)')
        for line in f:
            line = line.strip()
            class_id, class_description = class_matcher.match(line).groups()
            class_mapping[class_id] = class_description

    video_fps = {}
    with open(video_frames_info_path) as f:
        video_frames_info_reader = csv.DictReader(f)
        for row in video_frames_info_reader:
            video_fps[row['video']] = float(row['fps'])

    annotations = []
    with open(input_annotations_path) as f:
        annotations_reader = csv.DictReader(f)
        for row in annotations_reader:
            if not row['actions']:
                continue
            video = row['id']
            subject = row['subject']
            quality = int(row['quality']) if row['quality'] else -1
            verified = True if row['verified'] == 'Yes' else False
            action_instances = row['actions'].split(';')
            frames_per_second = video_fps[video]
            for instance in action_instances:
                class_id, start_seconds, end_seconds = instance.split(' ')
                start_seconds = float(start_seconds)
                end_seconds = float(end_seconds)
                start_frame = floor(start_seconds * frames_per_second)
                end_frame = ceil(end_seconds * frames_per_second)
                annotations.append({
                    'filename': video,
                    'subject': subject,
                    'verified': verified,
                    'quality': quality,
                    'start_seconds': start_seconds,
                    'end_seconds': end_seconds,
                    'start_frame': start_frame,
                    'end_frame': end_frame,
                    'frames_per_second': frames_per_second,
                    'category': '%s-%s' % (class_id, class_mapping[class_id])
                })

    with open(output, 'wb') as f:
        json.dump(annotations, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input_annotations', required=True)
    parser.add_argument(
        '--charades_classes',
        required=True,
        help='File containing lines "<class_id> <class_description>"')
    parser.add_argument(
        '--video_frames_info',
        required=True,
        help='CSV of format <video_name>,<fps>[,<num_frames_in_video>]?')
    parser.add_argument('--output_annotation_json', required=True)
    args = parser.parse_args()
    main(args.input_annotations, args.charades_classes, args.video_frames_info,
         args.output_annotation_json)
