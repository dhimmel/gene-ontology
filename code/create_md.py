import os
import re
import xml.etree.ElementTree
import untangle

import jinja2
import requests


taxids = list()
for filename in os.listdir('annotations'):
    match = re.search(r'taxid_([0-9]+)', filename)
    taxids.append(int(match.groups()[0]))
taxids.sort()


formated_taxids = ','.join(map(str, taxids))
taxid_to_name = dict()
url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=taxonomy&id={}'.format(formated_taxids)
response = requests.get(url)
etree = xml.etree.ElementTree.fromstring(response.content)
for docsum in etree:
    taxid = None
    name = None
    for item in docsum.findall('Item'):
        if item.get('Name') == 'TaxId':
            taxid = item.text
        if item.get('Name') == 'ScientificName':
            name = item.text
    taxid_to_name[taxid] = name


with open('code/template.md') as read_file:
    template_str = read_file.read()
template = jinja2.Template(template_str)

output = template.render(taxids = taxids, taxid_to_name = taxid_to_name)

with open('README.md', 'w') as write_file:
    write_file.write(output)


