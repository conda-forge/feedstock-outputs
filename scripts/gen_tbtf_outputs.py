import sys
import pprint
import requests
import json

from conda_forge_tick.utils import load_graph

# 1. load the graph
gx = load_graph()

# 2. read the nodes
with open("../feedstock-outputs/scripts/tbtf_nodes.txt", "r") as fp:
    tbtf_nodes = [n.strip() for n in fp.readlines()]

# 3. add things that seem to be missed...
tbtf_nodes = set(tbtf_nodes)
tbtf_nodes.add("clang-compiler-activation")
tbtf_nodes.add("clang-win-activation")

seen = set()
tbtf_outputs = {}
for n in tbtf_nodes:
    tbtf_outputs[n] = set()
    if "feedstock_name" not in gx.nodes[n]["payload"]:
        print(n, gx.nodes[n]["payload"].data)
        sys.exit(1)
    assert n == gx.nodes[n]["payload"]["feedstock_name"]

    outs = gx.nodes[n]["payload"].get("outputs_names", [])
    if outs:
        for out in outs:
            tbtf_outputs[n].add(out)
    else:
        tbtf_outputs[n].add(n)

    if tbtf_outputs[n] & seen:
        for bado in tbtf_outputs[n] & seen:
            print("OUTPUT CONFLICT: %s" % bado)
            for k, v in tbtf_outputs.items():
                if bado in tbtf_outputs[k]:
                    print("    %s: %s" % (k, bado))

    seen |= tbtf_outputs[n]

# now put through libcfgraph to make sure we have the right names
tails = ["linux-64", "win-64", "osx-64", "linux-aarch64", "linux-ppc64le"]
for p in tbtf_outputs:
    final_outs = set()
    for out in tbtf_outputs[p]:
        if out.endswith("_"):
            for tail in tails:
                # a little special casing
                if p.startswith('ctng') and tail == 'osx-64':
                    continue

                if p == "clang-compiler-activation" and tail == "win-64":
                    continue

                r = requests.get(
                    "https://api.anaconda.org/package/conda-forge/%s%s" % (
                        out, tail))
                if r.status_code == 200:
                    final_outs |= set([out + tail])

            r = requests.get(
                "https://api.anaconda.org/package/conda-forge/%s%s" % (
                    out, ""))
            if r.status_code == 200:
                final_outs |= set([out])
        else:
            final_outs.add(out)
    if final_outs != tbtf_outputs[p]:
        print("MUNGED NEW OUTPUTS:", p)
    tbtf_outputs[p] = final_outs

with open("../feedstock-outputs/scripts/final_outputs.txt", "w") as fp:
    fp.write(pprint.pformat(tbtf_outputs))

for p in tbtf_outputs:
    with open("../feedstock-outputs/outputs/%s.json" % p, "w") as fp:
        json.dump({"outputs": list(tbtf_outputs[p])}, fp)
