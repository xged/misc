from lang_char_freqs import *

ccf = CommitCharFreqs(f=Path('.lang_char_freqs--CommitCharFreqs.pkl'))
# try:
#     ccf.add_repourls_lastupdated(max=True)
# finally:
#     ccf.dump()
#     print(len(ccf.load().d))

for repo in ccf.load().d:
    for cf in ccf.load().d[repo].d:
        print(cf)
