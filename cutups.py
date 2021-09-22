#!/usr/bin/env python
'''
Does cutups on input text. Text can be read from standard input, or a text file can be provided as an argument.

Input text is split into chunks, which are randomly reordered. The size of these chunks can be controlled with command line arguments
'''

import argparse
import fileinput
import random


def cutup(text, min_chunk_size, max_chunk_size):
    words = text.split()
    chunks = []
    ind = 0

    while ind < len(words):
        chunk_size = random.randint(min_chunk_size, max_chunk_size)
        chunks.append(' '.join(words[ind:(ind+chunk_size)]))
        ind += chunk_size

    random.shuffle(chunks)
    output = ' '.join(chunks)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='?', help='file containing text to cut up')
    chunk_size_arg_help = 'text will be cut up into chunks of size `min-chunk-size` to `max-chunk-size`'
    parser.add_argument('--min-chunk-size', '-m', default=1, type=int, help=chunk_size_arg_help)
    parser.add_argument('--max-chunk-size', '-M', default=5, type=int, help=chunk_size_arg_help)

    args = parser.parse_args()
    if args.min_chunk_size > args.max_chunk_size:
        raise ValueError('`min-chunk-size` cannot be larger than `max-chunk-size`')
    
    if args.file is None:
        text = ' '.join(line for line in fileinput.input())
    else:
        with open(args.file, 'r') as f:
            text = f.read()

    print(cutup(text, args.min_chunk_size, args.max_chunk_size))
