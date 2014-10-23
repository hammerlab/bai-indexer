#!/usr/bin/env python
'''Print out start:stop locations for each reference in a BAI file.'''
import json
import struct
import sys

# -- helper functions --

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


def extract_offsets(data_stream):
    data = data_stream
    magic = data.read(4)
    if magic != 'BAI\x01':
        raise ValueError('This is not a BAI file (missing magic)')

    minBlockIndex = 1000000000
    refs = []
    n_ref = read_int32(data)
    for i in range(0, n_ref):
        ref_start = data.tell()
        n_bin = read_int32(data)
        for j in range(0, n_bin):
            bin_id = read_uint32(data)
            n_chunk = read_int32(data)

            chunks = []
            for k in range(0, n_chunk):
                chunk_beg = read_uint64(data)
                chunk_end = read_uint64(data)

        n_intv = read_int32(data)
        intvs = []
        for j in range(0, n_intv):
            ioffset = read_uint64(data)
            if ioffset:
                bi = ioffset / 65536
                if ioffset % 65536 != 0:
                    bi += 65536
                minBlockIndex = min(minBlockIndex, bi)
        ref_end = data.tell()

        refs.append((ref_start, ref_end))


    # Undocumented field: # of unmapped reads
    # See https://github.com/samtools/hts-specs/pull/2/files
    try:
        num_unmapped = read_uint64(data)
    except struct.error:
        pass

    extra_bytes = data.read()
    if extra_bytes != '':
        raise ValueError('Extra data after expected EOF (%d bytes: %r)' % (len(extra_bytes), extra_bytes))

    return {
        'minBlockIndex': minBlockIndex,
        'chunks': refs
    }


if __name__ == '__main__':
    data = open(sys.argv[1], 'rb')
    out = extract_offsets(data)
    print json.dumps(out)
