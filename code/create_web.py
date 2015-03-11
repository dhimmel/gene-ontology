import os
import re
import json
import xml.etree.ElementTree
import itertools

import jinja2
import requests

import utilities


taxids = list()
for filename in os.listdir('annotations'):
    if not filename.startswith('taxid'):
        continue
    match = re.search(r'taxid_([0-9]+)', filename)
    taxids.append(int(match.groups()[0]))
taxids.sort()

taxlist = [{'taxid': taxid} for taxid in taxids]
taxdict = {x['taxid']: x for x in taxlist}

formated_taxids = ','.join(map(str, taxids))
taxid_to_name = dict()
url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=taxonomy&id={}'.format(formated_taxids)
response = requests.get(url)
etree = xml.etree.ElementTree.fromstring(response.content)
for docsum in etree:
    taxid = None
    name = None
    item_dict = {item.get('Name'): item.text for item in docsum.findall('Item')}
    taxid = int(item_dict['TaxId'])
    taxdict[taxid]['scientific_name'] = tem_dict['ScientificName']
    taxdict[taxid]['common_name'] = tem_dict['CommonName']
    taxdict[taxid]['division'] = tem_dict['Division']

prop_opts = ['prop', 'unprop']
coding_opts = ['all', 'coding']
vocab_opts = ['entrez', 'symbol']

for prop, vocab, coding in itertools.product(prop_opts, vocab_opts, coding_opts):
    print prop, vocab, coding
    table = list()
    for taxid in taxids:
        print taxid
        path = utilities.annotation_path(taxid, prop, vocab, coding)
        annotations = list(utilities.read_annotations(path))
        stats = utilities.annotation_stats(annotations)
        row = [taxid, taxdict[taxid]['scientific_name'], stats['terms'], stats['annotations'], path]
        table.append(row)
    
    # write json for DataTables
    json_file_name = 'summary-{}-{}-{}.json'.format(prop, vocab, coding)
    json_path = os.path.join('summaries', json_file_name)
    with open(json_path, 'w') as write_file:
        json_data = {'data': table}
        json.dump(json_data, write_file, indent = 2)

"""
with open('code/template.md') as read_file:
    template_str = read_file.read()
template = jinja2.Template(template_str)

output = template.render(taxids = taxids, taxlist = taxlist)

with open('index.md', 'w') as write_file:
    write_file.write(output)

"""
