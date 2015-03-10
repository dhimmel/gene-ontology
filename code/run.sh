# Download the Gene Ontology
wget --timestamping --directory-prefix download/ http://purl.obolibrary.org/obo/go/go-basic.obo

# Download the gene2go file producted by Entrez Gene
wget --timestamping --directory-prefix download/ ftp://ftp.ncbi.nih.gov/gene/DATA/gene2go.gz

# Download the gene_info.gz file of Entrez Genes
wget --timestamping --directory-prefix download/ ftp://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz

# Run python
python code/gene-ontology.py

# Run R
Rscript code/gene-ontology.R
