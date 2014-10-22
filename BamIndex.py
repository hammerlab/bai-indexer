#!/usr/bin/env python
'''Parser for BAI (BAM Index) files.'''
import struct
import sys


def unpack(stream, fmt):
    size = struct.calcsize(fmt)
    buf = stream.read(size)
    return struct.unpack(fmt, buf)[0]


def read_int32(stream):
    return unpack(stream, '<i')

def read_uint32(stream):
    return unpack(stream, '<I')

def read_uint64(stream):
    return unpack(stream, '<Q')




data = open(sys.argv[1], 'rb')
magic = data.read(4)
if magic != 'BAI\x01':
    raise ValueError('This is not a BAI file (missing magic)')

n_ref = read_int32(data)
print 'n_ref=%r' % n_ref
for i in range(0, n_ref):
    n_bin = read_int32(data)
    print '  n_bin=%d' % n_bin
    for j in range(0, n_bin):
        bin_id = read_uint32(data)
        n_chunk = read_int32(data)
        #print '    bin_id=%s  n_chunk=%s' % (bin_id, n_chunk)

        for k in range(0, n_chunk):
            chunk_beg = read_uint64(data)
            chunk_end = read_uint64(data)
            #print '      %s:%s' % (chunk_beg, chunk_end)

    n_intv = read_int32(data)
    print '  n_intv: %s' % n_intv
    for j in range(0, n_intv):
        ioffset = read_uint64(data)

# Undocumented field: # of unmapped reads
# See https://github.com/samtools/hts-specs/pull/2/files
try:
    num_unmapped = read_uint64(data)
    print 'Unmapped reads: %d' % num_unmapped
except struct.error:
    pass

extra_bytes = data.read()
if extra_bytes != '':
    raise ValueError('Extra data after expected EOF (%d bytes: %r)' % (len(extra_bytes), extra_bytes))
