import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def read_json(path):
    with open(path) as f:
        data = json.load(f)
    return path.stem, data["feedstocks"]


def main(sources_dir, output_json):
    jsons = Path(sources_dir).glob("**/*.json")

    with ThreadPoolExecutor(4) as executor:
        all_packages = {pkg: repos for (pkg, repos) in executor.map(read_json, jsons)}
    print(f"Processed {len(all_packages)} packages.")
    output_json = Path(output_json)
    output_json.parent.mkdir(exist_ok=True, parents=True)
    with open(output_json, "w") as f:
        json.dump(all_packages, f, separators=(",", ":"), sort_keys=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sources_dir")
    parser.add_argument("output_json")
    args = parser.parse_args()

    sys.exit(main(args.sources_dir, args.output_json))
