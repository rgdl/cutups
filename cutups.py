#!/usr/local/bin/python
'''
Does cutups on text passed through standard input.

The input can be text on the command line:
e.g. echo "Example text Example text Example text" | ./cutups.py

Or a file:
e.g. cat "example_text.txt" | ./cutups.py
'''

import fileinput, random


raw_text = ""
for line in fileinput.input():
    raw_text += line

words = raw_text.split()
min_chunk_size = 1
max_chunk_size = 5
chunks = []
ind = 0

while ind < len (words):
    chunk_size = random.randint(min_chunk_size, max_chunk_size)
    chunks.append(' '.join(words[ind:(ind+chunk_size)]))
    ind += chunk_size

random.shuffle(chunks)
output = ' '.join(chunks)

print(output)
