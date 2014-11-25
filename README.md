[![Build Status](https://travis-ci.org/hammerlab/bai-indexer.svg?branch=master)](https://travis-ci.org/hammerlab/bai-indexer)

bai-indexer
===========

Build an index for your BAM Index (BAI).

Background
----------

[BAM][1] is a common file format for storing aligned reads from a gene
sequencing machine. These files can get enormous (100+ GB), so it's helpful to
have an index to support fast lookup.

[Samtools][2] defines a file format for a BAM index and provides a simple
command for generating one:

```
samtools index file.bam file.bam.bai
```

Unfortunately, these BAM Index (BAI) files can _also_ grow very large, often to
10 MB or more. When using a genome browser like [IGV][3] or [BioDalliance][4],
loading a large BAI file over a slow network is the unavoidable first step in
displaying alignment tracks.

bai-indexer solves this problem by building an index of your BAM Index. This is
a small JSON file which maps reference ID (i.e. chromosome number) to a byte
range within the BAI file. By loading the BAM index, a viewer can load only the
small subset of the BAM index that it actually needs.

Usage
-----

    pip install bai-indexer

    bai-indexer path/to/file.bam.bai > path/to/file.bam.bai.json

Format
------

The JSON index index looks like this:

```json
{
  "chunks": [
    [8, 716520],
    [716520, 1463832],
    [1463832, 2070072],
    ...
  ],
  "minBlockIndex": 1234
}
```

The first chunk (`[8, 716520]`) specifies the byte range in the BAI file which
describes the first ref (most likely `chr1` for a human genome). This is a
half-open `[start, stop)` interval.

The `minBlockIndex` field specifies the position of the first block in the BAM
file. Everything before this position is headers.

Development
-----------

After setting up a virtualenv, you can get going by running:

```bash
pip install -r requirements.txt
nosetests
```


[1]: https://github.com/samtools/hts-specs
[2]: http://www.htslib.org/
[3]: http://www.broadinstitute.org/igv/
[4]: http://www.biodalliance.org/
