#pytest

from lang_char_freqs import *

import string

    # def test_add_file(self):
    #     for fp in dir.glob('**/*'): self.addfp(fp, maxchars)

    # def rdf(self):
    #     return RepoDiffFreqs(fp=Path('._RepoFreqs-data-test.pkl'))

    # tmpdir =
    # git['clone', url, dir, '--depth=1', '--shallow-submodules'] & FG

# @pytest.fixture
# def tmp_repo():
#     rdftcf = RepoDiffFTCF(fp=Path('._RepoFreqs-data-test.pkl'), fpfresh=True)
#     rdf.addurls_(n_urls, 4, save_keep=True)

# def test_save_keep():
#     n_urls = 3
#     rdftcf = RepoDiffFTCF(fp=Path('._RepoFreqs-data-test.pkl'), fpfresh=True)
#     rdf.addurls_auto(n_urls, 4, save_keep=True)
#     assert len(rdf.read()) == n_urls

# def test_save_dump():
#     n_urls = 3
#     rdftcf = RepoDiffFTCF(fp=Path('._RepoFreqs-data-test.pkl'), fpfresh=True)
#     rdf.addurls_auto(n_urls, 4, save_dump=True)
#     assert len(rdf.read()) == n_urls

# def test_():
#     n_urls = 3
#     rdftcf = RepoDiffFTCF(fp=Path('._RepoFreqs-data-test.pkl'), fpfresh=True)
#     rdf.addurls_auto(n_urls, 4)
#     assert len(rdf) == n_urls

# def test_():
#     rdftcf = RepoDiffFTCF(fp=Path('._RepoFreqs-data-test.pkl'), fpfresh=True)
#     rdftcf.save()


    # def test_overwrite_read(self):
    #     n_urls = 2
    #     rdftcf = RepoDiffFTCF(fp=Path('._RepoFreqs-data-test.pkl'), fpfresh=True)
    #     rdf.addurls_(n_urls, 4)
    #     rdf.write()
    #     rdf.addurls_(n_urls, 4)
    #     rdf.write()
    #     self.assertEqual(rdf, rdf.read())

rdftcf = RepoDiffFTCF()
rdftcf.add_urls_lastupdated(npages=2, perpage=2, maxcommits=8, maxchars=2**12)
rdftcf.write(Path('._RepoFreqs-data-test.pkl'))
rdftcf.read(Path('._RepoFreqs-data-test.pkl'))
# print(rdftcf)

def test_subtotal():
    rdftcf.unicase()
    assert rdftcf.total(string.ascii_lowercase) == 0
    assert rdftcf.total() >= rdftcf.total("ETA") >= rdftcf.total("TA") >= 0

def test_flat():
    # print(rdftcf.flat)
    assert type(rdftcf.flat) == FileTypeCharFreqs
