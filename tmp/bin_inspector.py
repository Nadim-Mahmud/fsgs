"""Print the number of 3D points stored in COLMAP points3D.bin files."""

import argparse
from pathlib import Path
import struct


def count_points(path):
    # The first eight bytes hold a little-endian unsigned 64-bit count.
    with Path(path).open("rb") as stream:
        header = stream.read(8)
    if len(header) != 8:
        raise ValueError("Missing COLMAP point-count header")
    return struct.unpack("<Q", header)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths", nargs="*", type=Path,
        default=[
            Path("data/cameleon_random/distorted/sparse/0/points3D.bin"),
            Path("data/cameleon_random/sparse/0/points3D.bin"),
        ],
        help="COLMAP points3D.bin files to inspect",
    )
    args = parser.parse_args()
    failed = False
    for path in args.paths:
        try:
            print(f"{path}: {count_points(path):,} points")
        except (OSError, ValueError) as exc:
            print(f"{path}: ERROR: {exc}")
            failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
