import os
import json
# import gzip
# import sys

import pandas

import obonet # https://github.com/dhimmel/obonet
# csv.field_size_limit(sys.maxsize)

def read_entrez_file(path, column_names, dtype=None):
    """Read entrez text file format into a pandas.DataFrame"""
    return pandas.read_table(path, comment='#', names=column_names, na_values=['-'], dtype=dtype, index_col=False)

def read_gene2go(download_dir):
    """Read gene ontology annotations by Entrez"""
    path = os.path.join(download_dir, 'gene2go.gz')
    column_names = [
        'tax_id',
        'GeneID',
        'GO_ID',
        'Evidence',
        'Qualifier',
        'GO_term',
        'PubMed',
        'Category'
    ]
    return read_entrez_file(path, column_names)

def is_NOT_qaulifier(qualifier):
    """
    Returns whether a `Qualifier` in gene2go is a NOT qualifier.
    http://geneontology.org/page/go-annotation-conventions#not
    """
    if pandas.isnull(qualifier):
        return False
    if not qualifier:
        return False
    if qualifier.upper().startswith('NOT'):
        return True
    return False

def read_gene_info(download_dir):
    """Read entrez gene info as a pandas.DataFrame"""
    path = os.path.join(download_dir, 'gene_info.gz')
    column_names = [
        'tax_id',
        'GeneID',
        'Symbol',
        'LocusTag',
        'Synonyms',
        'dbXrefs',
        'chromosome',
        'map_location',
        'description',
        'type_of_gene',
        'Symbol_from_nomenclature_authority',
        'Full_name_from_nomenclature_authority',
        'Nomenclature_status',
        'Other_designations',
        'Modification_date',
    ]
    dtype = {x: str for x in column_names}
    for column in 'tax_id', 'GeneID':
        dtype[column] = int
    return read_entrez_file(path, column_names, dtype)

def read_go(download_dir):
    """Read the Gene Ontology from an OBO"""
    path = os.path.join(download_dir, 'go-basic.obo')
    with open(path) as read_file:
        graph = obonet.read_obo(read_file)
    return graph

def graph_to_dataframe(graph):
    """Create a dataframe of nodes"""
    rows = list()
    for node, data in graph.nodes(data=True):
        rows.append((node, data['name'], data['namespace']))
    go_df = pandas.DataFrame(rows, columns=['go_id', 'go_name', 'go_domain'])
    go_df = go_df.sort_values('go_id')
    return go_df

def get_annotation_path(annotation_dir, tax_id, ev_type, annotation_type, mkdir=False):
    directory = os.path.join(annotation_dir, 'taxid_{}'.format(tax_id))
    if mkdir and not os.path.isdir(directory):
        os.mkdir(directory)
    path = os.path.join(directory,
        'GO_annotations-{}-{}-{}.tsv'.format(tax_id, ev_type, annotation_type))
    return path

def read_annotation_df(path):
    df = pandas.read_table(path)
    for column in 'gene_ids', 'gene_symbols':
        df[column] = df[column].map(lambda x: str(x).split('|'))
    return df

def annotation_stats(annotation_df):
    stats = dict()
    stats['terms'] = len(annotation_df)
    stats['annotations'] = sum(annotation_df['size'])
    return stats

class Encoder(json.JSONEncoder):

    def default(self, o):
        if type(o).__module__ == 'numpy':
            return o.item()
        return json.JSONEncoder.default(self, o)

# def write_annotations(annotations, path, go_dag):
#     """Write annotations (a dict of term --> genes)"""
#     write_file = open(path, 'w')
#     writer = csv.writer(write_file, delimiter = '\t')
#     writer.writerow(['go_id', 'go_term', 'go_domain', 'size', 'genes'])
#     for term, genes in sorted(annotations.items()):
#         writer.writerow([term, go_dag[term].name, go_dag[term].namespace, len(genes), '|'.join(map(str, genes))])
#     write_file.close()
#
# def read_annotations(path):
#     """Read a tsv annotations file"""
#     read_file = open(path)
#     reader = csv.DictReader(read_file, delimiter = '\t')
#     for row in reader:
#         row['genes'] = row['genes'].split('|')
#         yield row
#     read_file.close()
#
# def annotation_path(taxid, prop, vocab, coding):
#     annotation_dir = os.path.join('annotations', 'taxid_{}'.format(taxid))
#     if not os.path.isdir(annotation_dir):
#         os.mkdir(annotation_dir)
#     path = os.path.join(annotation_dir,
#         'GO_annotations-{}-{}-{}-{}.tsv'.format(taxid, prop, vocab, coding))
#     return path
#
# def annotation_stats(annotations):
#     stats = dict()
#     sizes = [int(a['size']) for a in annotations]
#     stats['terms'] = len(annotations)
#     stats['annotations'] = sum(sizes)
#     return stats
