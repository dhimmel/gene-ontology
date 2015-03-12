import os
import re
import json
import time
import xml.etree.ElementTree
import itertools
import hashlib
import datetime
import time

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
    taxdict[taxid]['scientific_name'] = item_dict['ScientificName']
    taxdict[taxid]['common_name'] = item_dict['CommonName']
    taxdict[taxid]['division'] = item_dict['Division']

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


##

datetime_format = '%Y-%m-%d %H:%M:%S'
current_datetime = datetime.datetime.now().strftime(datetime_format)

files = list()
for filename in 'go-basic.obo', 'gene_info.gz', 'gene2go.gz':
    path = os.path.join('download', filename)
    ts_epoch = os.path.getmtime(path)
    mtime = datetime.datetime.fromtimestamp(ts_epoch).strftime(datetime_format)
    with open(path, 'rb') as read_file:
        hash_ = hashlib.sha1(read_file.read()).hexdigest()
    hash_ = hash_.upper()
    hash_ = ' '.join(a + b for a, b in zip(hash_[::2], hash_[1::2]))
    file_dict = {'filename': filename, 'hash': hash_, 'time': mtime}
    files.append(file_dict)

with open('code/files.html') as read_file:
    template_str = read_file.read()
template = jinja2.Template(template_str)

output = template.render(files = files, date = current_datetime)

with open('_includes/files.html', 'w') as write_file:
    write_file.write(output)



