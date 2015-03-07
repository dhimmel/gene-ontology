# Download the Gene Ontology
wget --timestamping --directory-prefix download/ http://purl.obolibrary.org/obo/go/go-basic.obo

# Download the gene2go file producted by Entrez Gene
wget --timestamping --directory-prefix download/ ftp://ftp.ncbi.nih.gov/gene/DATA/gene2go.gz

# Run python
python code/process.py

# Run R
Rscript code/visualize.R

#git commit -a -m "Update"
#git push origin master
