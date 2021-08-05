import pickle
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Set
from warnings import warn

import requests
from plumbum import FG, cmd
from whatthepatch import parse_patch

RepoUrl = str  # Github.com
FExten = str  # file extension (".py")

class CharFreqs():
    def __init__(self, d: Dict[FExten, Counter]=None) -> None:
        self.d = d or {}

    def append(self, fexten: FExten, counter: Counter) -> None:
        self.d[fexten] = self.d.get(fexten, Counter()) + counter

    def add(self, charfreqs: 'CharFreqs') -> None:
        for fexten in charfreqs.d:
            self.append(fexten, charfreqs.d[fexten])

    def unicase(self) -> None:
        for fexten in self.d:
            counter = Counter()
            for c in self.d[fexten]:
                counter.update({c.upper(): self.d[fexten][c]})
            self.d[fexten] = counter

    def total(self, chars: str=None) -> int:
        if chars is None:  # all chars
            return sum((sum(counter.values()) for counter in self.d.values()))
        return sum((counter[c] for c in chars for counter in self.d.values()))

    @property
    def uni_counter(self) -> Counter:
        return sum(self.d.values(), Counter())

class CommitCharFreqs():
    def __init__(self, d: Dict[RepoUrl, CharFreqs]=None, f: Path=None, commit_limit=1000, char_limit=1000, dupl='skip') -> None:
        assert dupl in ['add', 'replace', 'skip']
        self.d = d or {}
        self.f = f or Path('.CommitCharFreqs.pkl')
        self.commit_limit = commit_limit
        self.char_limit = char_limit
        self.dupl = dupl

    def append(self, repourl: RepoUrl, charfreqs: CharFreqs) -> None:
        if repourl in self.d:
            if self.dupl == 'add':
                self.d[repourl].add(charfreqs)
            elif self.dupl == 'replace':
                self.d[repourl] = charfreqs
            elif self.dupl == 'skip':
                return
            else:
                assert self.dupl in ['add', 'replace', 'skip']
        else:
            self.d[repourl] = charfreqs

    def add(self, ccf: 'CommitCharFreqs') -> None:
        for repourl in ccf.d:
            self.append(repourl, ccf.d[repourl])

    def add_commit(self, dir: Path, commithash, repourl: RepoUrl=None):
        repourl = repourl or cmd.git['-C', str(dir), 'remote', 'get-url', 'origin']()
        charfreqs = CharFreqs()
        for diff in parse_patch(cmd.git['-C', str(dir), 'diff', commithash]()):
            if diff.changes:
                addedlines = [l for loc, _, l in diff.changes if loc == None]
                charfreqs.append(Path(diff.header.new_path).suffix, Counter('\n'.join(addedlines[-self.char_limit:])))
        self.append(repourl, charfreqs)

    def add_dir(self, dir: Path, repourl: RepoUrl=None) -> None:
        repourl = repourl or cmd.git['-C', str(dir), 'remote', 'get-url', 'origin']()
        print(repourl, ':')
        commithashes = cmd.git['-C', str(dir), 'log', '-n', self.commit_limit, '--pretty=format:%H']().split()
        for i, commithash in enumerate(commithashes):
            self.add_commit(dir, commithash, repourl)
            print(i+1, "commits crunched.", end='\r')
        print()

    def add_repourl(self, repourl: RepoUrl) -> None:
        with TemporaryDirectory() as tempdir:
            cmd.git['clone', repourl, Path(tempdir), '--depth', self.commit_limit, '--shallow-submodules'] & FG
            self.add_dir(Path(tempdir), repourl)

    def add_repourls_lastupdated(self, npages=1, perpage=1, max=False) -> None:
        for repourl in fetch_repourls_lastupdated(npages, perpage, max):
            self.add_repourl(repourl)

    def load(self) -> 'CommitCharFreqs':
        with self.f.open('rb') as file:
            ccf = pickle.load(file)
        assert type(ccf) == type(self)
        if ccf.d == {}:
            warn("Object is empty.")
        return ccf

    def dump(self) -> None:
        print("Writing to {!r}...".format(self.f))
        with self.f.open('wb') as file:
            pickle.dump(self, file)

    def unicase(self) -> None:
        for repourl in self.d:
            self.d[repourl].unicase()

    def total(self, chars: str=None) -> int:
        if chars is None:  # all chars
            return sum((self.d[fexten].total() for fexten in self.d))
        return sum((ccf.total(chars) for ccf in self.d.values()))

    @property
    def uni_counter(self) -> Counter:
        return sum((ccf.uni_counter for ccf in self.d.values()), Counter())

    @property
    def uni_charfreqs(self) -> CharFreqs:
        charfreqs = CharFreqs()
        for cf in self.d.values():
            charfreqs.add(cf)
        return charfreqs

def fetch_repourls_lastupdated(npages=1, perpage=1, max=False) -> Set[RepoUrl]:
    if max:
        npages = 10; perpage = 100
        nresults = 1000
    else:
        assert npages >= 1 and perpage in range(1, 100+1)
        nresults = npages * perpage
        if nresults > 1000:
            warn("Github API limit: 1,000 search results", RuntimeWarning)
    print("Fetching {} recently updated Github repo urls...".format(nresults))
    repourls = set()
    for pagenr in range(1, npages + 1):
        r = requests.get('https://api.github.com/search/repositories',
                         {'q': 'stars:>0', 'sort': 'updated', 'per_page': perpage, 'page': pagenr})
        for item in r.json().get('items', {}):
            repourls.add(item.get('clone_url', None))
    return repourls
