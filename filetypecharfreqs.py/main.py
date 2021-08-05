from fty import RepoDiffCharFreqs

rdcf = RepoDiffCharFreqs()
rdcf.addurls_lastupdated(npages=1, perpage=1, maxcommits=4, fresh=True)
print(rdcf.read())
