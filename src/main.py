from argparse import ArgumentParser
import gzip
import os
from pathlib import Path

signatures = dict()
compressed = dict()


def parse_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--dataset", required=True, type=str)
    arg_parser.add_argument("--target", required=True, type=str)
    return arg_parser.parse_args()


def get_signature(path: Path):
    base_name = os.path.basename(path)
    os.system(f"./bin/GetMaxFreqs -w tmp/{base_name}.freqs {path}")

    with open(f"tmp/{base_name}.freqs", "rb") as file:
        return file.read()


if __name__ == "__main__":
    args = parse_args()

    target_signature = get_signature(args.target)

    print(len(target_signature))

    for path in Path("datasets").rglob("*.wav"):
        signatures[os.path.basename(path)] = get_signature(path)

    min_len = len(min(signatures.items(), key=lambda i: len(i[1]))[1])

    for (file_name, signature) in signatures.items():
        combined_signature = signature[0:min_len] + target_signature
        compressed[file_name] = len(gzip.compress(combined_signature))

    print(compressed)
