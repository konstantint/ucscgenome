'''
Simple access to the reference genomes at UCSC.
Tests for genome file location routine.

Copyright 2013, Konstantin Tretyakov.
http://kt.era.ee/

Licensed under MIT license.
'''

import os, pytest, shutil
from tempfile import mkdtemp
from ucscgenome.genome import open_genome_file, GenomeException

# This test requires creating directories, downloading files, etc, so
# sometimes we don't care to wait and just skip it.
SKIP_TEST = False

SOURCE_URL_PATTERN='http://kt.era.ee/%(id)s'

def setup_module(module):
    global root_dir, cache_dir, start_dir
    if SKIP_TEST:
        return
    start_dir = os.path.abspath(os.curdir)
    root_dir = mkdtemp()
    cache_dir = os.path.join(root_dir, 'cache')
    assert not os.path.exists(cache_dir)
    os.chdir(root_dir)

def teardown_module(module):
    if SKIP_TEST:
        return
    os.chdir(start_dir)
    shutil.rmtree(root_dir)

def test_open_genome_file():
    if SKIP_TEST:
        return
    # No-web, no-cache, must raise an exception
    with pytest.raises(GenomeException):
        f = open_genome_file('hg19', cache_dir=None, use_web=False)
    assert not os.path.exists(cache_dir)
    
    # No-web, cache, nonexistent search dir, must raise exception
    with pytest.raises(GenomeException):
        f = open_genome_file('hg19', cache_dir=cache_dir, use_web=False)
    assert not os.path.exists(cache_dir)

    # Web, cache, but file is also present in local dir, so no download
    f = open('hg19.2bit', 'w')
    f.write('##test##')
    f.close()
    f = open_genome_file('hg19', cache_dir=cache_dir, use_web=True)
    assert not os.path.exists(cache_dir)
    assert f.read() == '##test##'
    f.close()
    f = open_genome_file('hg19.2bit', cache_dir=cache_dir, use_web=True)
    assert not os.path.exists(cache_dir)
    assert f.read() == '##test##'
    f.close()
    os.unlink(f.name)    
    
    # Web, nonexistent file.
    with pytest.raises(GenomeException):
        f = open_genome_file('blablabla', cache_dir=cache_dir, source_url_pattern=SOURCE_URL_PATTERN)
    
    # Web, file not present in cache, must download
    progress_log = []
    f = open_genome_file('index.html', cache_dir=cache_dir, source_url_pattern=SOURCE_URL_PATTERN, reporthook=lambda c,b,t: progress_log.append(c))
    assert len(progress_log) != 0
    assert f.read(9) == '<!DOCTYPE'
    f.close()
    
    # Now same request, but file already in cache
    progress_log = []
    f = open_genome_file('index.html', cache_dir=cache_dir, source_url_pattern=SOURCE_URL_PATTERN, reporthook=lambda c,b,t: progress_log.append(c))
    assert len(progress_log) == 0
    assert f.read(9) == '<!DOCTYPE'
    f.close()
    
    # Now same request, but file also in local dir
    f = open('index.html', 'w')
    f.write('#test#')
    f.close()
    f = open_genome_file('index.html', cache_dir=cache_dir, source_url_pattern=SOURCE_URL_PATTERN, reporthook=lambda c,b,t: progress_log.append(c))
    assert len(progress_log) == 0
    assert f.read(6) == '#test#'
    f.close()
