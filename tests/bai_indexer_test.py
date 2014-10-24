from nose.tools import *

from bai_indexer import index_stream

import StringIO


def test_file_a():
    eq_({
            'chunks': [(8, 88), (88, 168), (168, 248), (248, 256)],
            'minBlockIndex': 217
        }, index_stream(open('tests/test_input_1_a.bam.bai')))


def test_file_b():
    eq_({
            'chunks': [(8, 16), (16, 96), (96, 176), (176, 184)],
            'minBlockIndex': 224
        }, index_stream(open('tests/test_input_1_b.bam.bai')))


def test_file_c():
    eq_({
            'chunks': [(8, 88), (88, 168)],
            'minBlockIndex': 177
        }, index_stream(open('tests/test_input_1_c.bam.bai')))


def test_stdin():
    # sys.stdin only has a read() method.
    stream = open('tests/test_input_1_c.bam.bai')
    class FakeStdin(object):
        read = stream.read

    eq_({
            'chunks': [(8, 88), (88, 168)],
            'minBlockIndex': 177
        }, index_stream(FakeStdin()))
