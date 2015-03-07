import os
import gzip
import csv

import goatools.obo_parser

go_path = os.path.join('download', 'go-basic.obo')
go_dag = goatools.obo_parser.GODag(obo_file = go_path)

def sort_dict_values(dictionary):
    """Sort each value of a dictionary."""
    for key, value in dictionary.items():
        dictionary[key] = sorted(value)

# Read Entrez Gene GO annotations
taxid_to_gene2go = dict()
gene2go_path = os.path.join('download', 'gene2go.gz')
gene2go_fields = 'tax_id', 'GeneID', 'GO_ID', 'Evidence', 'Qualifier', 'GO_term', 'PubMed', 'Category'
with gzip.open(gene2go_path) as read_file:
    row_generator = (row for row in read_file if not row.startswith('#'))
    reader = csv.DictReader(row_generator, delimiter='\t', fieldnames = gene2go_fields)
    for row in reader:
        taxid_to_gene2go.setdefault(row['tax_id'], list()).append(row)

for taxid, gene2go in taxid_to_gene2go.iteritems():
    print 'Initiating taxid', taxid

    # create a term --> genes (unpropogated) dictionary
    annotations = dict()
    for annotation in gene2go:
        term = annotation['GO_ID']
        gene_id = int(annotation['GeneID'])
        annotations.setdefault(term, set()).add(gene_id)
    sort_dict_values(annotations)
    len(annotations)

    # create a gene --> terms (unpropogated) dictionary
    gene_to_terms = dict()
    for term, genes in annotations.iteritems():
        for gene in genes:
            gene_to_terms.setdefault(gene, set()).add(term)
    len(gene_to_terms)


    # update gene_to_terms with propagated terms
    go_dag.update_association(gene_to_terms)

    annotations_prop = dict()
    for gene, terms in gene_to_terms.iteritems():
        for term in terms:
            annotations_prop.setdefault(term, set()).add(gene)
    sort_dict_values(annotations_prop)

    def write_annotations(annotations, path):
        """Write annotations (a dict of term --> genes)"""
        write_file = open(path, 'w')
        writer = csv.writer(write_file, delimiter = '\t')
        writer.writerow(['go_id', 'go_term', 'go_domain', 'size', 'genes'])
        for term, genes in sorted(annotations.items()):
            writer.writerow([term, go_dag[term].name, go_dag[term].namespace, len(genes), ';'.join(map(str, genes))])
        write_file.close()

    annotation_dir = os.path.join('annotations', 'taxid_{}'.format(taxid))
    if not os.path.isdir(annotation_dir):
        os.mkdir(annotation_dir)

    path = os.path.join(annotation_dir, 'annotations-unprop.tsv')
    write_annotations(annotations, path)

    path = os.path.join(annotation_dir, 'annotations-prop.tsv')
    write_annotations(annotations_prop, path)
