#!/usr/bin/env python
"""
Does cutups on input text. Text can be read from standard input, or a text file can be provided as an argument.

Input text is split into chunks, which are randomly reordered. The size of these chunks can be controlled with command line arguments
"""

import math
import random
import re
import sys
from dataclasses import dataclass
from functools import reduce
from itertools import product
from typing import Self

LINE_LENGTH = 80

# TODO: more tests to make sure it reconstructs chunks accurately


@dataclass
class TextChunk:
    text: str
    line_length: int

    def __post_init__(self) -> None:
        self.text = re.sub(r"\s+", " ", self.text)

    @property
    def lines(self) -> list[str]:
        if not hasattr(self, "_lines"):
            self._lines: list[str] = []
            text = self.text

            for _ in range(1000):
                text_head = text[:self.line_length]

                if text_head == text:
                    self._lines.append(text)
                    break

                if " " in text_head:
                    cut_point = self.line_length - text_head[::-1].index(" ") - 1
                    self._lines.append(text_head[:cut_point])
                else:
                    cut_point = self.line_length - 1
                    self._lines.append(text_head[:cut_point] + "-")

                text = text[cut_point:].lstrip(" ")
            else:
                raise RuntimeError("Max iterations reached")

        return self._lines

    def split(self, output_line_length: int, output_n_lines: int) -> list[Self]:
        output: list[Self] = []
        line_groups: list[list[str]] = []
        chunks_per_line_group = math.ceil(
            self.line_length / output_line_length
        )

        # put lines into groups

        lines = list(self.lines)  # Copy to avoid mutating the original lines

        while lines:
            line_groups.append(lines[:output_n_lines])
            lines = lines[output_n_lines:]

        # split each line in each chunk

        for lg in line_groups:
            lg_results = ["" for _ in range(chunks_per_line_group)]

            for i, line in product(range(chunks_per_line_group), lg):
                start = i * output_line_length
                end = (i + 1) * output_line_length
                lg_results[i] += line[start:end]

            for lg_result in lg_results:
                output.append(self.__class__(lg_result, output_line_length))

        expected_n_outputs = math.ceil(
            self.line_length / output_line_length
        ) * math.ceil(len(self.lines) / output_n_lines)

        assert len(output) == expected_n_outputs

        return output

    def vjoin(self, other: Self) -> Self:
        return self.__class__(self.text + " " + other.text, self.line_length)


    def cutup(self, output_line_length: int, output_n_lines: int) -> Self:
        n_cols = math.ceil(self.line_length / output_line_length)
        n_rows = math.ceil(len(self.lines) / output_n_lines)

        splits = self.split(output_line_length, output_n_lines)
        random.shuffle(splits)

        split_iter = iter(splits)

        arranged_splits = [
            [next(split_iter) for _ in range(n_cols)]
            for _ in range(n_rows)
        ]
        arranged_cols: list[Self] = []

        for c in range(n_cols):
            arranged_cols.append(
                reduce(
                    lambda a, b: a.vjoin(b),
                    (row[c] for row in arranged_splits),
                )
            )

        total_output_lines = max(len(x.lines) for x in arranged_cols)
        new_text = ""

        for line in range(total_output_lines):
            for col in arranged_cols:
                try:
                    new_text += col.lines[line] + " "
                except IndexError:
                    pass
        
        return self.__class__(new_text, self.line_length)



    def __repr__(self) -> str:
        return "\n".join(line for line in self.lines)


if __name__ == "__main__":
    try:
        texts: list[str] = []

        for file in sys.argv[1:]:
            with open(file, "r") as f:
                texts.append(f.read())

    except IndexError:
        texts = [" ".join(line for line in sys.stdin)]

    tc = TextChunk(" ".join(texts), LINE_LENGTH)
    print(tc.cutup(LINE_LENGTH // 2, 10))
