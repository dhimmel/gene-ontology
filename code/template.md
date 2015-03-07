---
title: Annotating the Gene Ontology with Entrez Genes
---
# Annotating the Gene Ontology with Entrez Genes

## Download annotations by species
{% for taxid in taxids %}
+ {{ taxid_to_name[taxid] }} taxid_{{ taxid }}: [propogated](https://raw.githubusercontent.com/dhimmel/gene-ontology/master/annotations/taxid_{{ taxid }}/annotations-prop.tsv), [unpropogated](https://raw.githubusercontent.com/dhimmel/gene-ontology/master/annotations/taxid_{{ taxid }}/annotations-prop.tsv){% endfor %}

