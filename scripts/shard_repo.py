#!/usr/bin/env python
"""
run this script from the top-level dir of the repo
"""

import os
import glob
import json
import subprocess
import sys
import tqdm


try:
    with open("config.json") as f:
        config = json.load(f)
except Exception:
    print("no config.json found, using defaults", file=sys.stderr)
    config = {
        "outputs_path": "outputs",
        "shard_level": 3,
        "shard_fill": "z"
    }

outputs_path = config["outputs_path"]
shard_level = config["shard_level"]
shard_fill = config["shard_fill"]


outputs = glob.glob(f"{outputs_path}/*.json")

for orig_out in tqdm.tqdm(outputs):
    out = os.path.basename(orig_out)
    chars = [c for c in out if c.isalnum()]
    while len(chars) < shard_level:
        chars.append(shard_fill)

    final_pth = os.path.join(outputs_path, *chars[:shard_level])
    os.makedirs(final_pth, exist_ok=True)
    final_out = os.path.join(final_pth, out)

    tqdm.tqdm.write("moving %s to %s" % (orig_out, final_out))

    subprocess.run(
        ["cp", orig_out, final_out],
        check=True
    )
