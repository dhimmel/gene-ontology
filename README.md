# User-friendly Gene Ontology annotations

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.21711.svg)](https://doi.org/10.5281/zenodo.21711)

This project provides easy-to-use [Gene Ontology](http://geneontology.org/) annotations. Annotations relate GO Terms with [Entrez Genes](https://doi.org/10.1093/nar/gki031). We provide genes as Entrez GeneIDs and as symbols.

Users choose from the following options:

+ species: which species to retrieve annotations for
+ evidence: whether to use all annotations or annotations from experimental evidence only
+ propagation: whether to include only direct annotations or infer annotations based on ontology structure

The project includes a [website](https://git.dhimmel.com/gene-ontology/) for browsing and downloading annotation files.

## Execution

`sh code/run.sh > log.txt` downloads the latest input resources and rebuilds the annotation data.
