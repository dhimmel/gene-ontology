#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e


# Download the Gene Ontology
wget --timestamping --directory-prefix download/ http://purl.obolibrary.org/obo/go/go-basic.obo

# Download the gene2go file producted by Entrez Gene
wget --timestamping --directory-prefix download/ ftp://ftp.ncbi.nih.gov/gene/DATA/gene2go.gz

# Download the gene_info.gz file of Entrez Genes
wget --timestamping --directory-prefix download/ ftp://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz


# Run python
python code/process.py
python code/create_web.py

# Run R
#Rscript code/gene-ontology.R

# For local development, run
#jekyll serve


# Commit
#git pull
#git commit -a -m "Updates"
#git push origin gh-pages
