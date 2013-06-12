'''
Simple access to the reference genomes at UCSC.
Main class tests.

Copyright 2013, Konstantin Tretyakov.
http://kt.era.ee/

Licensed under MIT license.
'''

from ucscgenome.genome import Genome

# This test requires downloading or having the sacCer2 in cache
SKIP_TEST = False

def test_genome_data():
    if SKIP_TEST:
        return
    g = Genome('sacCer2')
    assert str(g['chrI'][0:10]) == 'CCACACCACA'
    assert str(g['chrIV'][99:109]) == 'CACACCCACA'
    assert len(g) == 18
    # Check against http://hgdownload.cse.ucsc.edu/goldenPath/sacCer2/database/chromInfo.txt.gz
    chromInfo = '''chrIV	1531919	/gbdb/sacCer2/sacCer2.2bit
chrXV	1091289	/gbdb/sacCer2/sacCer2.2bit
chrVII	1090947	/gbdb/sacCer2/sacCer2.2bit
chrXII	1078175	/gbdb/sacCer2/sacCer2.2bit
chrXVI	948062	/gbdb/sacCer2/sacCer2.2bit
chrXIII	924429	/gbdb/sacCer2/sacCer2.2bit
chrII	813178	/gbdb/sacCer2/sacCer2.2bit
chrXIV	784333	/gbdb/sacCer2/sacCer2.2bit
chrX	745742	/gbdb/sacCer2/sacCer2.2bit
chrXI	666454	/gbdb/sacCer2/sacCer2.2bit
chrV	576869	/gbdb/sacCer2/sacCer2.2bit
chrVIII	562643	/gbdb/sacCer2/sacCer2.2bit
chrIX	439885	/gbdb/sacCer2/sacCer2.2bit
chrIII	316617	/gbdb/sacCer2/sacCer2.2bit
chrVI	270148	/gbdb/sacCer2/sacCer2.2bit
chrI	230208	/gbdb/sacCer2/sacCer2.2bit
chrM	85779	/gbdb/sacCer2/sacCer2.2bit
2micron	6318	/gbdb/sacCer2/sacCer2.2bit'''
    for ln in chromInfo.split('\n'):
        chrName, chrLen, _ = ln.split()
        assert len(g[chrName]) == int(chrLen)
    g.close()