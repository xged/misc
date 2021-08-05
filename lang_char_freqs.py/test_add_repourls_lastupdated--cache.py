from pathlib import Path

import pytest

from lang_char_freqs import CommitCharFreqs


@pytest.mark.order1
def test_add_repourls_lastupdated(arg):
    ccf = CommitCharFreqs(f=Path(".test_add_repourls_lastupdated.pkl"), commit_limit=8)
    ccf.add_repourls_lastupdated(npages=1, perpage=4)
    new_total = ccf.total()
    old_total = ccf.load().total()
    ccf.load()
    assert ccf.load().total() == new_total + old_total
