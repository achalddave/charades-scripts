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

from parsing import parse_annotations


def main(input_annotations_path, video_frames_info_path, charades_classes_path,
         output):
    annotations = parse_annotations(
        input_annotations_path, video_frames_info_path, charades_classes_path)
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
    main(args.input_annotations, args.video_frames_info, args.charades_classes,
         args.output_annotation_json)
