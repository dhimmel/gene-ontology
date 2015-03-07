---
title: Annotating the Gene Ontology with Entrez Genes
---
# Annotating the Gene Ontology with Entrez Genes

## Download annotations by species
{% for taxid in taxids %}
+ {{ taxid_to_name[taxid] }} taxid_{{ taxid }}: [propogated](annotations/taxid_{{ taxid }}/annotations-prop.tsv), [unpropogated](annotations/taxid_{{ taxid }}/annotations-prop.tsv){% endfor %}

