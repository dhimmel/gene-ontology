#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Retrieve changes
git pull origin gh-pages

# Download the Gene Ontology
wget --timestamping --directory-prefix download/ http://purl.obolibrary.org/obo/go/go-basic.obo

# Download the gene2go file producted by Entrez Gene
wget --timestamping --directory-prefix download/ ftp://ftp.ncbi.nih.gov/gene/DATA/gene2go.gz

# Download the gene_info.gz file of Entrez Genes
wget --timestamping --directory-prefix download/ ftp://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz

# Run python
runipy --overwrite code/process.ipynb
python code/create_web.py

# # Commit
# git add --all
# git commit -m "Update with new data releases"
# git push origin gh-pages
