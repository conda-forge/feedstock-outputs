# feedstock-outputs

registry of feedstock outputs

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
