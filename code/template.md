---
title: Annotating the Gene Ontology with Entrez Genes
---
# Annotating the Gene Ontology with Entrez Genes

## Download annotations by species

| taxid  | scientific_name | propagated | unpropogated |
| ------ | --------------- | ---------- | ------------ |
{% for taxelem in taxlist -%}
| {{taxelem.taxid}} | *{{taxelem.scientific_name}}* | [download](annotations/taxid_{{taxelem.taxid}}/annotations-prop.tsv) | [unpropogated](annotations/taxid_{{taxelem.taxid}}/annotations-prop.tsv) |
{% endfor %}

