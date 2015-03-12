import os
import csv
import gzip
import sys

csv.field_size_limit(sys.maxsize)

def read_entrez_file(path, fieldnames):
    """ """
    read_file = gzip.open(path)
    row_generator = (row for row in read_file if not row.startswith('#'))
    reader = csv.DictReader(row_generator, delimiter='\t', fieldnames = fieldnames)
    for row in reader:
        for key, value in row.items():
            if value == '-':
                row[key] = None
        yield row
    read_file.close()

def read_gene2go(exclude_NOT_qualifier = True):
    fieldnames = 'tax_id', 'GeneID', 'GO_ID', 'Evidence', 'Qualifier', 'GO_term', 'PubMed', 'Category'
    path = os.path.join('download', 'gene2go.gz')
    row_generator = read_entrez_file(path, fieldnames)
    if exclude_NOT_qualifier:
        row_generator = (row for row in row_generator if row['Qualifier'] != 'NOT')
    return row_generator

def read_gene_info():
    fieldnames = ['tax_id', 'GeneID', 'Symbol', 'LocusTag', 'Synonyms',
    'dbXrefs', 'chromosome', 'map_location', 'description',
    'type_of_gene', 'Symbol_from_nomenclature_authority',
    'Full_name_from_nomenclature_authority', 'Nomenclature_status',
    'Other_designations', 'Modification_date']
    path = os.path.join('download', 'gene_info.gz')
    return read_entrez_file(path, fieldnames)

def write_annotations(annotations, path, go_dag):
    """Write annotations (a dict of term --> genes)"""
    write_file = open(path, 'w')
    writer = csv.writer(write_file, delimiter = '\t')
    writer.writerow(['go_id', 'go_term', 'go_domain', 'size', 'genes'])
    for term, genes in sorted(annotations.items()):
        writer.writerow([term, go_dag[term].name, go_dag[term].namespace, len(genes), '|'.join(map(str, genes))])
    write_file.close()

def read_annotations(path):
    """Read a tsv annotations file"""
    read_file = open(path)
    reader = csv.DictReader(read_file, delimiter = '\t')
    for row in reader:
        row['genes'] = row['genes'].split('|')
        yield row
    read_file.close()

def annotation_path(taxid, prop, vocab, coding):
    annotation_dir = os.path.join('annotations', 'taxid_{}'.format(taxid))
    if not os.path.isdir(annotation_dir):
        os.mkdir(annotation_dir)
    path = os.path.join(annotation_dir,
        'GO_annotations-{}-{}-{}-{}.tsv'.format(taxid, prop, vocab, coding))
    return path

def annotation_stats(annotations):
    stats = dict()
    sizes = [int(a['size']) for a in annotations]
    stats['terms'] = len(annotations)
    stats['annotations'] = sum(sizes)
    return stats
