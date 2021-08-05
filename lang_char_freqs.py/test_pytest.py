import string
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from warnings import warn

from lang_char_freqs import CommitCharFreqs


def test_add_dir():
    global ccf
    ccf = CommitCharFreqs(commit_limit=50)
    for path in Path("test_data").iterdir():
        if path.is_dir():
            ccf.add_dir(path)

def test_add_repourls_lastupdated():
    CommitCharFreqs(commit_limit=4).add_repourls_lastupdated()

def test_total():
    ccf2 = deepcopy(ccf)
    ccf2.unicase()
    assert ccf2.total(string.ascii_lowercase) == 0
    if ccf2.total("E") == 0:
        warn("Strange results!", RuntimeWarning)
    else:
        assert ccf2.total("ETA") > ccf2.total("TA") >= 0
    assert ccf2.total() == ccf.uni_charfreqs.total() == sum(ccf2.uni_counter.values()) > 0

def test_charfreqs():
    charfreqs = next(iter(ccf.d.values()))
    if charfreqs.total() == 0:
        warn("Strange results!", RuntimeWarning)
    assert charfreqs.total() == sum(charfreqs.uni_counter.values())

def test_add():
    ccf2 = deepcopy(ccf)
    ccf2.add(ccf)
    assert ccf2.total() == 2 * ccf.total() and len(ccf2.d) == len(ccf.d)
    ccf2.dupl = 'skip'
    ccf2.add(ccf)
    assert ccf2.total() == 2 * ccf.total() and len(ccf2.d) == len(ccf.d)
    ccf2.dupl = 'replace'
    ccf2.add(ccf)
    assert ccf2.total() == ccf.total() and len(ccf2.d) == len(ccf.d)

def test_file():
    with TemporaryDirectory() as tempdir:
        ccf2 = deepcopy(ccf)
        ccf2.store = Path(tempdir) / Path("_.pkl")
        ccf2.dupl = 'replace'
        ccf2.load()
        assert ccf2.load().total() == ccf.total()
        ccf2 = deepcopy(ccf)
        ccf2.store = Path(tempdir) / Path("_.pkl")
        ccf2.load()
        assert ccf2.load().total() == 2 * ccf.total()
        ccf2.dump()
        assert ccf2.load().d == {}
