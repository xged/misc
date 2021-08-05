from lang_char_freqs import *

ccf = CommitCharFreqs(commit_limit=200)
for path in Path("data").iterdir():
    ccf.add_dir(path)
