# feedstock-outputs

registry of feedstock outputs

Each json blob maps the conda package (in the name of the json blob) to the feedstocks that produce it (in the "feedstocks" list in the json blob contants). 

If you make a change so that a package is produced by a different feedstock, please make a PR adding the feedstock name to the contents of the json blob for the package.
