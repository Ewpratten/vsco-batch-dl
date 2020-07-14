# vsco-batch-dl
A script for downloading a batch of images from VSCO

## Installing

```sh
python3 setup.py install --user
```

## Usage

```sh
$ python3 -m vsco_batch_dl -h

usage: vsco-batch-dl [-h] [-u USER] [-f FILE] [-o OUT]

A script for downloading a batch of images from VSCO

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User account to download from
  -f FILE, --file FILE  File containing urls to download from
  -o OUT, --out OUT     Output directory
```