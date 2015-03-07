---
title: Annotating the Gene Ontology with Entrez Genes
---
# Annotating the Gene Ontology with Entrez Genes

## Download annotations by species

| taxid  | scientific_name | download | download |
| ------ | --------------- | -------- | -------- |
{% for taxelem in taxlist -%}
| {{taxelem.taxid}} | *{{taxelem.scientific_name}}* | [prop](annotations/taxid_{{taxelem.taxid}}/annotations-prop.tsv) | [unprop](annotations/taxid_{{taxelem.taxid}}/annotations-prop.tsv) |
{% endfor %}

