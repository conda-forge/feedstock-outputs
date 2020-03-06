import networkx as nx
from conda_forge_tick.utils import load_graph


def _get_feedstock(p, gx, output_to_feedstock):
    fs = None
    if p in gx.nodes:
        _p = p
    elif (
        p in output_to_feedstock and
        output_to_feedstock[p] in gx.nodes
    ):
        _p = output_to_feedstock[p]
    else:
        print("UNKNOWN OUTPUT: pkg=%s output=%s" % (pkg, p))

    if not gx.nodes[_p]["payload"].get("archived", False):
        fs = _p

    return fs


# 1. load the graph
gx = load_graph()

# 2. constrct mapping of outputs to feedstocks
output_to_feedstock = {
    output: name
    for name, node in gx.nodes.items()
    for output in node.get("payload", {}).get("outputs_names", [])
}

# 3. get deps of key packages and big deps
init_tbtf_packages = set()

# get deps of some key packages
for pkg in ["conda", "conda-build", "conda-smithy"]:
    _tbtf = set()
    with gx.nodes[pkg]["payload"] as attrs:
        for _, v in attrs["requirements"].items():
            for p in v:
                fs = _get_feedstock(p, gx, output_to_feedstock)
                if fs is not None:
                    _tbtf.add(fs)

    init_tbtf_packages |= _tbtf

# more than 5% of everything
percent = .05
min_dec = int(len(gx) * percent)
for n in gx.nodes:
    if len(nx.descendants(gx, n)) > min_dec:
        fs = _get_feedstock(n, gx, output_to_feedstock)
        if fs is not None:
            init_tbtf_packages.add(fs)

# 4. now add all ancestors of those
_anc = set()
for p in init_tbtf_packages:
    anc = nx.ancestors(gx, p)
    for a in anc:
        fs = _get_feedstock(a, gx, output_to_feedstock)
        if fs is not None:
            _anc.add(fs)

tbtf_packages = _anc | init_tbtf_packages

# 5. print and save
for p in sorted(list(tbtf_packages)):
    print("   ", p)

with open("../feedstock-outputs/scripts/tbtf_nodes.txt", "w") as fp:
    for p in sorted(list(tbtf_packages)):
        fp.write("%s\n" % p)
