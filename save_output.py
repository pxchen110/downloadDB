import os
import csv
import zipfile
from zipfile import ZipFile


def saveOutput(out_path, gene_list, db_source, pathway_name):
    if 'kegg' in db_source:
        db = 'KEGG'
    elif 'harmo' in db_source:
        db = 'Harmonizome'
    if '+' in pathway_name:
        pathway_name = pathway_name.replace('+','_')
    
    out_prefix = '{}_{}'.format(db, pathway_name)
    
    with open(os.path.join(out_path,'{}_gene_list.txt'.format(out_prefix)), 'w') as fw:
        fw.write('#Query Database: {}\n'.format(db))
        fw.write('#Query Pathway ID: {}\n'.format(pathway_name))

        for element in gene_list:
            fw.write('{}\n'.format(element))

    with open(os.path.join(out_path,'{}_gene_list.csv'.format(out_prefix)), 'w', newline= '') as fw:
        csv.writer(fw)
        fw.write('#Query Database: {}\n'.format(db))
        fw.write('#Query Pathway ID: {}\n'.format(pathway_name))
        for element in gene_list:
            fw.write('{}\n'.format(element))

    return out_prefix

def saveZipOutput(out_path, out_prefix, out_file_list):
    with ZipFile(os.path.join(out_path, '{}.zip'.format(out_prefix)), 'w') as fz:
        for file in out_file_list:
            fz.write(os.path.join('query_output', '{}_gene_list.txt'.format(file)))
    #return out_prefix


if __name__ == '__main__':
    saveOutput()