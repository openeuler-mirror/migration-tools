#!/usr/bin/env python3
import argparse

"""
replace string of file1 with context of file2, and write to output file
"""

def parse_args():
    parser = argparse.ArgumentParser(description='Replace string of file1 with context of file2')
    parser.add_argument("-f1", "--file1", help="File1", required=True)
    parser.add_argument("-f2", "--file2", help="File2", required=True)
    parser.add_argument("-s", "--string", help="String to replace", required=True)
    parser.add_argument("-o ", "--output", help="Output file", required=True)

    return parser.parse_args()

def replace_string_with_file(file1, file2, string, output):
    with open(file1, 'r') as f1, open(file2, 'r') as fs:
        with open(output, 'w') as fo:
            fo.write(f1.read().replace(string, fs.read()))

if __name__ == "__main__":
    args = parse_args()
    replace_string_with_file(args.file1, args.file2, args.string, args.output)