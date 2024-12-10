#!/usr/bin/env python
"""A CLI using typer to perform cutups on text."""
import random
import re
from itertools import cycle
from pathlib import Path

import typer


def format(text: str, line_length: int = 30) -> list[str]:
    """Remove existing line breaks and format into a block of lines.
    
    N.B. this is a basic implementation, which allows lines to be a little
    longer than `line_length`.
    """
    output: list[str] = []
    line_words: list [str] = []

    for word in re.split(r"\s+", text):
        line_words.append(word)
        line = " ".join(line_words)

        if len(line) > line_length:
            output.append(line)
            line_words = []

    return output


def main(
    files: list[Path], paragraph_size: int = 4, random_offset: bool = True
) -> None:
    match len(files):
        case 1:
            file1 = files[0]
            file2 = files[0]
        case 2:
            file1, file2 = files
        case _:
            raise ValueError("Can't handle 3 or more input files")

    text1 = format(file1.read_text())
    text2 = format(file2.read_text())

    if random_offset:
        offset1 = random.randint(0, len(text1) - 1)
        text1 = text1[offset1:] + text1[:offset1]
        offset2 = random.randint(0, len(text2) - 1)
        text2 = text2[offset2:] + text2[:offset2]

    if len(text1) > len(text2):
        text_iter1 = iter(text1)
        text_iter2 = cycle(text2)
    elif len(text1) < len(text2):
        text_iter1 = cycle(text1)
        text_iter2 = iter(text2)
    else:
        text_iter1 = iter(text1)
        text_iter2 = iter(text2)

    for i, (l1, l2) in enumerate(zip(text_iter1, text_iter2)):
        if i > 0 and i % paragraph_size == 0:
            print()
        print(l1, l2)


if __name__ == "__main__":
    typer.run(main)

