
Does cutups on input text. Text can be read from standard input, or a text file can be provided as an argument.

Input text is split into chunks, which are randomly reordered. The size of these chunks can be controlled with command line arguments

```bash
./cutups.py text-file.txt

# OR

echo "here is some text to cut up" | ./cutups.py 
```
