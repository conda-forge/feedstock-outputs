import argparse
import json
import re
import sys
from base64 import b64decode
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def read_json(path):
    with open(path) as f:
        data = json.load(f)
    return path.stem, data["feedstocks"]


def fetch_cdts():
    import requests

    r = requests.get("https://api.github.com/repos/conda-forge/cdt-builds/contents/README.md")
    r.raise_for_status()
    data = r.json()
    text = b64decode(data["content"]).decode()
    seen = set()
    for result in re.finditer(r"\(https://anaconda\.org/conda-forge/([a-z0-9_\-\.\+]+)\)", text):
        if result and result.group(1) not in seen:
            seen.add(result.group(1))
            yield result.group(1)


def main(sources_dir, output_json, with_cdts=False):
    jsons = Path(sources_dir).glob("**/*.json")

    with ThreadPoolExecutor(4) as executor:
        all_packages = {pkg: repos for (pkg, repos) in executor.map(read_json, jsons)}
    print(f"Processed {len(all_packages)} packages.")

    if with_cdts:
        for cdt in fetch_cdts():
            all_packages.setdefault(cdt, []).append("cdt-builds")

    output_json = Path(output_json)
    output_json.parent.mkdir(exist_ok=True, parents=True)
    with open(output_json, "w") as f:
        json.dump(all_packages, f, separators=(",", ":"), sort_keys=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sources_dir")
    parser.add_argument("output_json")
    parser.add_argument("--with-cdts", action="store_true")
    args = parser.parse_args()

    sys.exit(main(args.sources_dir, args.output_json, with_cdts=args.with_cdts))
