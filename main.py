#!/usr/bin/env python3
"""Entry for make.fun news-image-20261125.

Copies the pre-rendered front page (entry.png, in this repository) to
/output/entry.png. Deterministic: no clock, no randomness, no network.
Only the standard library is used, so nothing needs installing.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_size(path):
    """Read width/height from a PNG IHDR chunk without any image library."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_MAGIC or head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    if not os.path.isfile(SRC):
        print("missing source image: entry.png", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print("source image over 1 MiB: %d bytes" % size, file=sys.stderr)
        return 1
    dims = png_size(SRC)
    if dims is None:
        print("source image is not a PNG", file=sys.stderr)
        return 1
    if dims[0] > MAX_SIDE or dims[1] > MAX_SIDE:
        print("source image over 1024x1024: %dx%d" % dims, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("wrote %s (%dx%d, %d bytes)" % (DST, dims[0], dims[1],
                                          os.path.getsize(DST)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
