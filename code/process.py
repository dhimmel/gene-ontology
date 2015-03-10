import os
import gzip
import csv
import itertools

import goatools.obo_parser

import utilities

go_path = os.path.join('download', 'go-basic.obo')
go_dag = goatools.obo_parser.GODag(obo_file = go_path)

def sort_dict_values(dictionary):
    """Sort each value of a dictionary."""
    for key, value in dictionary.items():
        dictionary[key] = sorted(value)

# Read Entrez Gene GO annotations
taxid_to_gene2go = dict()
for row in utilities.read_gene2go():
    taxid_to_gene2go.setdefault(row['tax_id'], list()).append(row)

taxids = set(taxid_to_gene2go)

# Read gene info
coding_genes = set()
gene_to_symbol = dict()
print 'Reading Entrez Gene Info'
for row in utilities.read_gene_info():
    if row['tax_id'] not in taxids:
        continue
    gene = int(row['GeneID'])
    if row['type_of_gene'] == 'protein-coding':
        coding_genes.add(gene)
    gene_to_symbol[gene] = row['Symbol']


prop_opts = ['prop', 'unprop']
coding_opts = ['all', 'coding']
vocab_opts = ['entrez', 'symbol']

# Iterate by species
for taxid, gene2go in taxid_to_gene2go.iteritems():
    print 'Initiating taxid', taxid

    # create a term --> genes (unpropogated) dictionary
    annotations_unprop = dict()
    for annotation in gene2go:
        term = annotation['GO_ID']
        gene_id = int(annotation['GeneID'])
        annotations_unprop.setdefault(term, set()).add(gene_id)
    len(annotations_unprop)

    # create a gene --> terms (unpropogated) dictionary
    gene_to_terms = dict()
    for term, genes in annotations_unprop.iteritems():
        for gene in genes:
            gene_to_terms.setdefault(gene, set()).add(term)
    len(gene_to_terms)

    # update gene_to_terms with propagated terms
    go_dag.update_association(gene_to_terms)

    annotations_prop = dict()
    for gene, terms in gene_to_terms.iteritems():
        for term in terms:
            annotations_prop.setdefault(term, set()).add(gene)
    
    for prop, vocab, coding in itertools.product(prop_opts, vocab_opts, coding_opts):
        if prop == 'prop':
            annotations = annotations_prop.copy()
        if prop == 'unprop':
            annotations = annotations_unprop.copy()
        if coding == 'coding':
            for goid, genes in annotations.items():
                annotations[goid] = genes & coding_genes
        if vocab == 'symbol':
            for goid, genes in annotations.items():
                symbols = {gene_to_symbol[gene] for gene in genes}
                symbols.discard(None)
                annotations[goid] = symbols
        for goid, genes in annotations.items():
            if not genes:
                del annotations[goid]
        sort_dict_values(annotations)

        path = utilities.annotation_path(taxid, prop, vocab, coding)
        utilities.write_annotations(annotations, path, go_dag)

print 'complete'
