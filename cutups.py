#!/usr/bin/env python
"""
Does cutups on input text. Text can be read from standard input, or a text file can be provided as an argument.

Input text is split into chunks, which are randomly reordered. The size of these chunks can be controlled with command line arguments
"""

import argparse
import random
import sys

LINE_LENGTH = 80


def cutup(text: str, min_chunk_size: int, max_chunk_size: int) -> str:
    """
    Cut text into chunks, each containing a number of words in the range [min_chunk_size, max_chunk_size]

    These chunks will then be re-joined in a random order and returned as a string
    """
    words = text.split()
    chunks = []
    ind = 0

    while ind < len(words):
        chunk_size = random.randint(min_chunk_size, max_chunk_size)
        chunks.append(" ".join(words[ind:(ind+chunk_size)]))
        ind += chunk_size

    random.shuffle(chunks)
    return " ".join(chunks)


def add_line_breaks(text: str, line_length: int = LINE_LENGTH) -> list[str]:
    lines: list[str] = []

    while text:
        text_head = text[:line_length]

        if " " in text_head:
            cut_point = line_length - text_head[::-1].index(" ") - 1
            lines.append(text_head[:cut_point])
        else:
            cut_point = line_length - 1
            lines.append(text_head[:cut_point] + "-")

        text = text[cut_point:]

    return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="file containing text to cut up")
    chunk_size_arg_help = (
        "text will be cut up into chunks of size `min-chunk-size` to "
        "`max-chunk-size`"
    )
    parser.add_argument(
        "--min-chunk-size", "-m", default=1, type=int, help=chunk_size_arg_help
    )
    parser.add_argument(
        "--max-chunk-size", "-M", default=5, type=int, help=chunk_size_arg_help
    )

    args = parser.parse_args()

    if args.min_chunk_size > args.max_chunk_size:
        raise ValueError(
            "`min-chunk-size` cannot be larger than `max-chunk-size`"
        )
    
    if args.file is None:
        text = " ".join(line for line in sys.stdin)
    else:
        with open(args.file, "r") as f:
            text = f.read()

    result = cutup(text, args.min_chunk_size, args.max_chunk_size)

    for line in add_line_breaks(result):
        print(line)
