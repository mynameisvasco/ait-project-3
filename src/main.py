from argparse import ArgumentParser
import gzip
import lzma
import bz2
import os
from pathlib import Path


signatures = dict()
ncd = dict()


def parse_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--dataset", required=True, type=str)
    arg_parser.add_argument("--target", required=True, type=str)
    arg_parser.add_argument("--compression", required=False, type=str,
                            choices=['gzip', 'bzip2', 'lzma'])
    return arg_parser.parse_args()


def get_signature(path: Path):
    base_name = os.path.basename(path)
    os.system(f"./bin/GetMaxFreqs -w tmp/{base_name}.freqs {path}")

    if Path(f"tmp/{base_name}.freqs").exists():
        with open(f"tmp/{base_name}.freqs", "rb") as file:
            return file.read()


def calculate_ncd(item1: str, item2: str, compressor=gzip):
    item1_compressed = compressor.compress(item1)
    item2_compressed = compressor.compress(item2)
    concatenated = item1 + item2
    concatenated_compression = gzip.compress(concatenated)
    return (len(concatenated_compression) - min(len(item1_compressed), len(item2_compressed))) / \
        max(len(item1_compressed), len(item2_compressed))


if __name__ == "__main__":
    args = parse_args()

    if args.compression == "bzip2":
        compressor = bz2
    else:
        if args.compression == "lzma":
            compressor = lzma
        else:
            compressor = gzip

    target_signature = get_signature(args.target)
    target_compressed = gzip.compress(target_signature)

    for path in Path("datasets").rglob("*.wav"):
        signatures[os.path.basename(path)] = get_signature(path)

    for (file_name, signature) in signatures.items():
        ncd[file_name] = calculate_ncd(signature, target_signature, gzip)

    print(min(ncd.items(), key=lambda n: n[1]))
