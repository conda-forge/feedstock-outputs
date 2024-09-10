# feedstock-outputs

registry of feedstock outputs

## Configuration

The JSON blob [`config.json`](config.json) contains the configuration for the feedstock outputs registry. The configuration contains the following fields:

- outputs_path: the path to the sharded outputs in the repo
- shard_level: how deeply the outputs are sharded
- shard_fill: the character to use to fill in sharding levels for outputs
  with names shorter than shard_level
- auto_register_all: whether to automatically register new outputs for any feedstock

The `auto_register_all` boolean is used by the `conda-forge-webservices` and `conda-forge-ci-setup` packages to determine if new outputs should be automatically registered. If `auto_register_all` is `true`, then any new outputs for feedstock
will be automatically added. If it is `false`, then only those that match the glob patterns (as described below) will be added.

## Format

Each json blob maps the conda package (in the name of the json blob) to the feedstocks that produce it (in the "feedstocks" list in the json blob contants).

## Automatic Registration of Outputs that Follow Regular Patterns

Some feedstocks output packages that have a regular pattern (e.g., `llvdmdev` outputs `libllvm19`, `libllvm20`, etc.).
We store a list of allowed output glob patterns in this [file](feedstock_outputs_autoreg_allowlist.yml). Each entry
is a list of allowed glob patterns for the feedstock. These patterns are tested against new outputs using the Python
`fnmatch` module. If a feedstock uploads a package that matches one of these patterns, the output is automatically
registered.

## Adding New Outputs and Glob Patterns

If you make a change so that a package is produced by a different feedstock or adds an output, please make a PR
using the [admin-requests repo](https://github.com/conda-forge/admin-requests?tab=readme-ov-file#add-a-package-output-to-a-feedstock) to add the new output. You can add new glob patterns via the [admin-requests repo](https://github.com/conda-forge/admin-requests?tab=readme-ov-file#add-a-package-output-to-a-feedstock) as well.
