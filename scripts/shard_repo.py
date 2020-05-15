#!/usr/bin/env python
"""
run this script from the top-level dir of the repo
"""

import os
import glob
import subprocess
import tqdm


outputs = glob.glob("outputs/*.json")

for orig_out in tqdm.tqdm(outputs):
    out = os.path.basename(orig_out)
    chars = [c for c in out if c.isalnum()]
    while len(chars) < 3:
        chars.append("z")

    final_pth = os.path.join("outputs", chars[0], chars[1], chars[2])
    os.makedirs(final_pth, exist_ok=True)
    final_out = os.path.join(final_pth, out)

    tqdm.tqdm.write("moving %s to %s" % (orig_out, final_out))

    subprocess.run(
        ["cp", orig_out, final_out],
        check=True
    )
